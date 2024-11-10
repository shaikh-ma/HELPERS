import ast
import importlib
import inspect
import os
import shutil


def add_file_extension(path, ext="py"):
    """
    Returns the path with extention added.

    Parameters
    ----------
    path: str
      Path string to which extention should be added.
    ext: str, default 'py'
      The extention string to be added to given path.

    Returns
    ----------
    path: str
      Path string with extension added.
    """
    if not path.endswith(f".{ext}"):
        path = f"{path}.{ext}"
    return path


def remove_file_extension(path, ext="py"):
    """
    Removes the extention from given path string.

    Parameters
    ----------
    path: str
      Path string from which extention should be removed.

    ext: str, default 'py'
      The extention string to be removed from given path.

    Returns
    ----------
    path: str
      Path string with the extenion removed.
    """
    if path.endswith(f".{ext}"):
        path = path.replace(f".{ext}", "")
    return path


def take_file_backup(file_path, to_path=None):
    """
    Creates a backup of given file and saves it to given path.

    Parameters
    ----------
    file_path: str
      The path of the file which needs to be backup.
    to_path: str, default None
      The destination path where the backup file should be saved.
      If not passed, it will be same as `file_path`.

    Returns
    ----------
    str:
      The path where the backup file is stored.

    """
    to_path = to_path or file_path
    return shutil.copyfile(file_path, to_path + ".bak")


def import_module_from_path(module_path):
    """
    Imports a module and returns an object that can be
    interpreted using the `inspect` module.

    Parameters
    ----------
    module_path: str
      Folder path where the module is saved.

    Returns
    ----------
    module: object
      The object that can be interpreted using `inspect` library.

    """
    module_path = add_file_extension(module_path)

    # Check if the file exists
    if not os.path.isfile(module_path):
        err = f"The specified module path does not exist: {module_path}"
        raise FileNotFoundError(err)

    # Get the module name (without .py)
    module_name = os.path.basename(module_path)
    module_name = remove_file_extension(module_name)

    # Load the module
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_functions_in_module(module_path):
    """
    Extract a list of all functions present in the module.
    It excludes protected functions & methods of a class.
    """
    module = import_module_from_path(module_path)
    return [
        obj
        # (name, str(inspect.signature(obj)))
        # for name, obj in inspect.getmembers(module)
        for _, obj in inspect.getmembers(module)
        if inspect.isfunction(obj) and obj.__module__ == module.__name__
    ]


def get_methods_in_module(module_path):
    """
    Extract a list of all methods present in the module.
    It excludes protected methods of a class.
    """
    module = import_module_from_path(module_path)
    methods_list = []

    submembers = [obj for _, obj in inspect.getmembers(module) if inspect.isclass(obj)]

    for member in submembers:
        if inspect.isclass(member):
            for _, obj in inspect.getmembers(member):
                if inspect.isfunction(obj) and obj.__module__ == module.__name__:
                    methods_list.append(obj)
    return methods_list


class RaiseVisitor(ast.NodeVisitor):
    def __init__(self):
        self.raises = []

    def visit_Raise(self, node):
        # Check if the raise statement has an exception
        if isinstance(node.exc, ast.Call):
            # Get the exception type (e.g., ValueError)
            exc_type = node.exc.func.id if isinstance(node.exc.func, ast.Name) else None

            # Get the message (if it's a string)
            if node.exc.args and isinstance(node.exc.args[0], ast.Str):
                message = node.exc.args[0].s  # Get the string message
                self.raises.append((exc_type, message))
        self.generic_visit(node)  # Continue visiting other nodes


def find_raise_statements(source_code):
    """
    Returns a tuple containing the exceptions raised.

    Parameters
    ----------
    source_code: str
      The script to be scanned for finding our raised exceptions.

    Returns
    ----------
    list[tuple]:
      List containing the number of raise statement and the message (if any).

    """
    # Create a RaiseVisitor instance and visit the AST
    visitor = RaiseVisitor()
    visitor.visit(ast.parse(source_code))
    return visitor.raises
