import inspect

from . import utils


def guess_obj_type(def_val):
    """
    Attempts to identify the type of a variable or object.

    Parameters
    ----------
    def_val: str
      The object who's type need to be determined.

    Returns
    ----------
    def_type: str
      The assumed type of the given variable.
    """
    def_type = ""
    if def_val in ("True", "False"):
        def_type = "bool"
    elif def_val.startswith("[") and def_val.endswith("]"):
        def_type = "list"
    elif def_val.startswith("(") and def_val.endswith("]"):
        def_type = "tuple"
    elif def_val.startswith("'") and def_val.endswith("'"):
        def_type = "str"
    elif def_val.startswith('"') and def_val.endswith('"'):
        def_type = "str"

    if len(def_type) > 0:
        def_type += ","
    return def_type


def add_docstring_to_function(function):
    """
    Returns the placeholder docstring for a given function.

    Parameters
    ----------
    function: function object
      The function who's docstring is to be generated.

    Returns
    ----------
    docstring: str
      The placeholder docstring with needed sections that can be
      added to a given function.
      It uses numpy standard.

    """
    existing_doc = inspect.getdoc(function)
    source_code = inspect.getsource(function)
    raises = utils.find_raise_statements(source_code)
    signature = str(inspect.signature(function))
    signature = signature.replace("(", "")
    signature = signature.replace(")", "")
    signature = list(filter(lambda x: x.strip(), signature.split(", ")))

    if not existing_doc:
        docstring = '\n    """\n'
        docstring += f"    {function.__name__} - Description"

        if signature:
            args_list = []
            for arg in signature:
                if "=" in arg:
                    def_type = ""
                    arg, def_val = arg.split("=")
                    def_type = guess_obj_type(def_val)
                    args_list.append(f"    {arg}: {def_type} default {def_val}")
                else:
                    args_list.append(f"    {arg}: ")
            args_list = "\n\n".join(args_list) + "\n"
            docstring += "\n\n    Parameters\n    ----------\n"
            docstring += args_list

        if raises:
            raises = list(filter(lambda x: x, raises))
            docstring += "\n\n    Raises\n    ----------\n"
            docstring += "\n\n".join([f"    {x[0]}: " for x in raises])

        source_code_list = source_code.split("\n")
        source_code_list = [
            line.strip().replace("return ", "")
            for line in source_code_list
            if "return " in line
        ]
        source_code_list = [f"    {line}: " for line in source_code_list]
        source_code_list = "\n\n".join(source_code_list) + "\n"

        docstring += "\n\n    Returns\n    ----------\n"
        docstring += source_code_list
        docstring += '\n    """\n'
    else:
        docstring = existing_doc

    return docstring
