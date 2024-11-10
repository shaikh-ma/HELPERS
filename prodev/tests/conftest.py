import pytest

from prodev.helpers import utils

EXAMPLE_MODULE = "./tests/example_module.py"


@pytest.fixture(scope="session")
def functions_list():
    return utils.get_functions_in_module(EXAMPLE_MODULE)
