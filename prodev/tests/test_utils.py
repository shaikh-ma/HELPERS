import inspect
import os

import pytest

from prodev.helpers import utils

from .conftest import EXAMPLE_MODULE


def test_get_functions_in_module(functions_list):
    assert all(filter(inspect.isfunction, functions_list))


def test_import_module_from_path():
    module = utils.import_module_from_path(EXAMPLE_MODULE)
    assert module.__name__ == "example_module"

    with pytest.raises(FileNotFoundError):
        utils.import_module_from_path("EXAMPLE_MODULE")


def test_take_file_backup():
    x = utils.take_file_backup(EXAMPLE_MODULE)
    assert x == "./tests/example_module.py.bak"
    os.remove(x)


def test_get_methods_in_module():
    actual = utils.get_methods_in_module(EXAMPLE_MODULE)
    assert all(filter(inspect.isfunction, actual))


def test_defined_exceptions(functions_list):
    for function in functions_list:
        source_code = inspect.getsource(function)
        raises = utils.find_raise_statements(source_code)
        assert isinstance(raises, list)


def test_add_file_extension():
    actual = utils.add_file_extension("test")
    assert actual == "test.py"
