import os
import sys

from helpers import autotests, utils

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


test_dir = os.path.join(root_dir, "tests")


if not os.path.exists(test_dir):
    os.mkdir(test_dir)

# store only .py files
py_modules_list = [
    utils.remove_file_extension(x)
    for x in modules_list
    if x.endswith(".py") and not x.startswith("__")
]


for module in py_modules_list:
    print("=" * 70)
    print("Module: ", module)
    print("=" * 70)
    module_path = os.path.join(root_dir, module)

    # check test modules exists for modules is the list
    test_module_name = os.path.join(test_dir, f"test_{module}.py")

    if not os.path.exists(test_module_name):
        # Extract all functions from module
        needed_imports = []
        template_tests_list = []
        functions_list = utils.get_functions_in_module(module_path)
        methods_list = utils.get_methods_in_module(module_path)

        exceptions_list = [
            autotests.create_placeholder_exception_tests(function)
            for function in functions_list
        ]

        exceptions_list = list(filter(lambda x: x, exceptions_list))

        if functions_list:
            needed_imports.append(f"import {module}")
            template_tests_list.extend(
                [
                    autotests.create_placeholder_function_tests(function)
                    for function in functions_list
                ]
            )
        if methods_list:
            class_name = methods_list[0].__qualname__.split(".")[0]
            needed_imports.append(f"from {module} import {class_name}")
            template_tests_list.extend(
                [
                    autotests.create_placeholder_method_tests(method)
                    for method in methods_list
                ]
            )

        if exceptions_list:
            needed_imports.append("import pytest")
            template_tests_list.extend(
                [
                    autotests.create_placeholder_exception_tests(function)
                    for function in functions_list
                ]
            )

        # print(template_tests_list)

        if len(template_tests_list) > 0:
            # Add template test functions to the test module
            with open(test_module_name, "w") as test_module:
                print("Adding template tests...")
                test_module.write("\n".join(needed_imports) + "\n\n")
                test_module.write("\n".join(template_tests_list))
