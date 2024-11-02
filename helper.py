import importlib
import inspect
import os
import shutil

TEST_FUNCTION_TEMPLATE = """
def test_{name}():
    actual = {module}.{name}{sign}
    assert actual == expected
"""

TEST_METHOD_TEMPLATE = """
def test_{name}():
    {_class}_obj = {_class}()
    actual = {_class}.{name}{sign}
    assert actual == expected
"""

TEST_FUNCTION_EXCPETIONS_TEMPLATE = """
def test_{name}_validations():
    with pytest.raises({exc}, match="{err_msg}"):
        {module}.{name}{sign}
"""


def create_placeholder_exception_tests(function):
    """
    Returns template test for exceptions in a function.
    """
    source_code = inspect.getsource(function)
    raises = find_raise_statements(source_code)
    exceptions_list = []
    for exc, err_msg in raises:
        exceptions_list.append(
            TEST_FUNCTION_EXCPETIONS_TEMPLATE.format(
                name=function.__name__,
                module=function.__module__,
                sign=inspect.signature(function),
                exc=exc,
                err_msg=err_msg,
            )
        )
    exceptions_list = "\n".join(exceptions_list)
    return exceptions_list


def create_placeholder_method_tests(method):
    """
    """

    """
    Returns template test for class methods.
    """
    return TEST_METHOD_TEMPLATE.format(
        name=method.__name__,
        _class=method.__qualname__.split(".")[0],
        sign=str(inspect.signature(method))
        .replace("(self, ", "(")
        .replace("(self", "("),
    )


def create_placeholder_function_tests(function):
    """
    Returns a template tests for given function.
    """
    return TEST_FUNCTION_TEMPLATE.format(
        name=function.__name__,
        module=function.__module__,
        sign=inspect.signature(function),
    )


def add_file_extension(path, ext="py"):
    if not path.endswith(f".{ext}"):
        path = f"{path}.{ext}"
    return path


def remove_file_extension(path, ext="py"):
    if path.endswith(f".{ext}"):
        path = path.replace(f".{ext}", "")
    return path


def take_file_backup(file_path):
    return shutil.copyfile(file_path, file_path + ".bak")


def import_module_from_path(module_path):
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


def has_docstring(functions_list):
    return [func for func in functions_list if inspect.getdoc(func)]


# def validate_docstrings(function_list):
#     for func in function_list:
#         doc_cur = inspect.getdoc(func)
#         if doc_cur:
#             for sign in inspect.getfullargspec(func)[0]:
#                 print(doc_cur.find(sign))
#                 if doc_cur.find(sign) >= 0:
#                     print("Present: ", sign)
#         else:
#             print("missing_docstring")

#     return


# =======================================

import ast

# class RaiseVisitor(ast.NodeVisitor):
#     def __init__(self):
#         self.raises = []

#     def visit_Raise(self, node):
#         # Capture the raise statement
#         self.raises.append(node)
#         self.generic_visit(node)  # Continue visiting other nodes

# def find_raise_statements(source_code):
#     # Parse the source code into an AST
#     tree = ast.parse(source_code)

#     # Create a RaiseVisitor instance and visit the AST
#     visitor = RaiseVisitor()
#     visitor.visit(tree)

#     return visitor.raises


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
    # Create a RaiseVisitor instance and visit the AST
    visitor = RaiseVisitor()
    visitor.visit(ast.parse(source_code))
    return visitor.raises
