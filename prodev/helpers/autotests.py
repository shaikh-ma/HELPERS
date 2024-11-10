import inspect

from . import templates as templ
from . import utils


def create_placeholder_exception_tests(function):
    """
    Returns template test for exceptions in a function.
    """
    source_code = inspect.getsource(function)
    raises = utils.find_raise_statements(source_code)
    if not raises:
        return ""
    exceptions_list = []
    params = ""

    if len(raises) == 1:
        exc = raises[0][0]
        err_msg = f'"{raises[0][1]}"'
        test_param = ""
    elif len(raises) > 1:
        test_params_list = ["error", "err_msg"]
        exc = test_params_list[0]
        err_msg = test_params_list[1]
        test_param = ", ".join(test_params_list)
        params_list = [f'    ({exc}, "{err_msg}")' for exc, err_msg in raises]
        params_list = "\n" + ", \n".join(params_list)
        params = "\n@pytest.mark.parametrize(\n    "
        params += f'"{test_param}"' + ",\n"
        params = f"{params}    ({params_list}" + "\n    )\n)"

    exceptions_list.append(
        params
        + templ.TEST_FUNCTION_EXCEPTIONS_TEMPLATE.format(
            name=function.__name__,
            module=function.__module__,
            sign=inspect.signature(function),
            exc=exc,
            err_msg=err_msg,
            test_param=test_param,
        )
    )
    exceptions_list = "\n".join(exceptions_list)
    return exceptions_list


def create_placeholder_method_tests(method):
    """
    Returns template test for class methods.
    """
    return templ.TEST_METHOD_TEMPLATE.format(
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
    return templ.TEST_FUNCTION_TEMPLATE.format(
        name=function.__name__,
        module=function.__module__,
        sign=inspect.signature(function),
    )


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
