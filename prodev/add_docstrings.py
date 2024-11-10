import inspect
import os
import sys

from helpers import autodocs, utils

# User passes root directory path
if len(sys.argv) > 2:
    raise ValueError("Invalid input")

root_dir = sys.argv[1]

# Create a list of all modules present in the root directory
if os.path.isdir(root_dir):
    modules_list = os.listdir(root_dir)
else:
    module_name = os.path.split(root_dir)[-1]
    root_dir = root_dir.replace(module_name, "")
    modules_list = [module_name]

py_modules_list = [
    x for x in modules_list if x.endswith(".py") and not x.startswith("__")
]

backup_folder = os.path.join(root_dir, "file_backups")
if not os.path.exists(backup_folder):
    os.mkdir(backup_folder)

for module in py_modules_list:
    print(f"Working on {module}")
    utils.take_file_backup(
        os.path.join(root_dir, module), os.path.join(backup_folder, module)
    )
    module_path = os.path.join(root_dir, module)
    functions_list = utils.get_functions_in_module(module_path)
    methods_list = utils.get_methods_in_module(module_path)

    with open(module_path) as mod:
        contents = mod.read()

    for function in functions_list:
        if not function.__doc__:
            cur_docstring = autodocs.add_docstring_to_function(function)
            source_code = inspect.getsource(function)
            code, line_no = inspect.findsource(function)
            updated_code = source_code.replace(
                code[line_no], code[line_no].rstrip() + cur_docstring
            )
            contents = contents.replace(source_code, updated_code)

    with open(module_path, "w") as mod:
        mod.write(contents)
