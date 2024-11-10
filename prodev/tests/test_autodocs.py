from prodev.helpers import autodocs


def test_add_docstring_to_function(functions_list):
    for function in functions_list:
        updated_function = autodocs.add_docstring_to_function(function)
        assert updated_function.__doc__


# def test_guess_obj_type():
# assert autodocs.guess_obj_type('True') == 'bool,'
# assert autodocs.guess_obj_type('False') == 'bool,'
# assert autodocs.guess_obj_type("'test'") == 'str'
# assert autodocs.guess_obj_type('"str"') == 'str'
# assert autodocs.guess_obj_type(('str')) == 'tuple'
# assert autodocs.guess_obj_type(['str']) == 'list'
