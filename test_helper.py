import inspect
import os

import pytest

import helper

EXAMPLE_MODULE = "example_module.py"
expected = [
    """
def test_function1():
    actual = example_module.function1()
    assert actual == expected
""",
    """
def test_function2():
    actual = example_module.function2(arg1)
    assert actual == expected
""",
    """
def test_function3():
    actual = example_module.function3(arg1=None)
    assert actual == expected
""",
]


@pytest.fixture()
def functions_list():
    return helper.get_functions_in_module(EXAMPLE_MODULE)


def test_create_placeholder_function_tests(functions_list):
    for ind, val in enumerate(expected):
        assert helper.create_placeholder_function_tests(functions_list[ind]) == val


def test_get_functions_in_module(functions_list):
    assert all(filter(inspect.isfunction, functions_list))


def test_import_module_from_path():
    module = helper.import_module_from_path(EXAMPLE_MODULE)
    assert module.__name__ == "example_module"


def test_take_file_backup():
    x = helper.take_file_backup(EXAMPLE_MODULE)
    assert x == "example_module.py.bak"
    os.remove(x)


def test_get_methods_in_module():
    actual = helper.get_methods_in_module(EXAMPLE_MODULE)
    assert all(filter(inspect.isfunction, actual))


def test_has_docstring(functions_list):
    actual = helper.has_docstring(functions_list)
    assert len(actual) == 2


def test_defined_exceptions(functions_list):
    for function in functions_list:
        source_code = inspect.getsource(function)
        raises = helper.find_raise_statements(source_code)
        print(raises)


def test_create_placeholder_exception_tests(functions_list):
    for ind, val in enumerate(expected):
        helper.create_placeholder_exception_tests(functions_list[ind])
        # assert helper.create_placeholder_exception_tests(functions_list[ind]) == val