def function1():
    raise ValueError("Raising ValueError")
    return None


def function2(arg1):
    raise KeyError("Raising KeyError")
    return arg1


def function3(arg1=None, arg2=False):
    return arg1


def function4(arg1, arg2=[None], arg3=True):
    return arg1


class Example:
    """ Class docstring """

    def __init__(self, arg1, arg2, arg3=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def method1():
        """ Docstring for method1. """
        return None

    def method2(arg1):
        """ Docstring for method2. """
        return arg1

    def method3(arg1=None):
        """ Docstring for method3. """
        return arg1


class Example2:
    """ Class docstring """

    def __init__(self, arg1, arg2, arg3=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def method1():
        """ Docstring for method1. """
        return None

    def method2(arg1):
        """ Docstring for method2. """
        return arg1

    def method3(arg1=None):
        """ Docstring for method3. """
        return arg1
