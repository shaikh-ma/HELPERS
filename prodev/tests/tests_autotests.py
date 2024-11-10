from prodev.helpers import autotests

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
    actual = example_module.function3(arg1=None, arg2=False)
    assert actual == expected
""",
]


def test_create_placeholder_function_tests(functions_list):
    for ind, val in enumerate(expected):
        assert autotests.create_placeholder_function_tests(functions_list[ind]) == val


def test_create_placeholder_exception_tests(functions_list):
    for ind, val in enumerate(expected):
        autotests.create_placeholder_exception_tests(functions_list[ind])
        # assert helpers.create_placeholder_exception_tests(functions_list[ind]) == val
