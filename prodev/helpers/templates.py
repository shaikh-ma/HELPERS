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

TEST_FUNCTION_EXCEPTIONS_TEMPLATE = """
def test_{name}_validations({test_param}):
    error_msg = {err_msg}
    with pytest.raises({exc}, match=error_msg):
        {module}.{name}{sign}
"""
