"""

Yet Another Python Switch-Case


"""

from collections import defaultdict

#
# Utility classes.
#

class CaseCollectingDict(dict):
    """This is a dict subclass which adds the feature of saving the data
    passed to `__setitem__` calls for the key `_` to a dict.  It is set as the
    `__prepare__` method `SwitchMetaclass`."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["_fundict"] = defaultdict(list) # Non-string key: avoid clashes with attr names.

    def __setitem__(self, key, value):
        if hasattr(value, "_yapsc_id"):
            raise SwitchError("The 'case' decorator was called with no arguments."
                              " Use the '@default' decorator for the default case.")

        if isinstance(key, str) and isinstance(value, list) and key != "switch" and (
                                                                key == "_" or key[0] != "_"):
            fun, case_args = value
            if not case_args:
                self["_fundict"][()] = fun
            for arg in case_args:
                # Wrap `arg` in a tuple so the default case can have a unique `()` key.
                self["_fundict"][(arg,)].append(fun)
            super().__setitem__(key, staticmethod(fun)) # Set the fun as a staticmethod.

        else: # Allow arbitrary attrs to be set, but ignore them as part of switch.
            super().__setitem__(key, value)

#
# Decorator functions.
#

def case(*case_values):
    """The `case` decorator used in switch definitions."""
    if not case_values:
        raise SwitchError("No case arguments.  Use the '@default' decorator to"
                          " define the default case.")
    def process_case(fun):
        return [fun, case_values]
    process_case._yapsc_id = True # To detect when `case` is called with no parens.
    return process_case

def default(fun):
    """The `default` decorator used in switch definitions."""
    return [fun, []]

#
# The `Switch` metaclass and class.
#

class SwitchMetaclass(type):
    """Metaclass for the `Switch` class."""
    def __new__(mcs, name, bases, attrs, *, on=[]):
        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class

    @classmethod
    def __prepare__(mcs, name, bases, on=[]):
        """Return the dict-like object to be set as `__dict__` (i.e., to hold
        the class attributes)."""
        dct = CaseCollectingDict() # Saves data each time a case is defined.
        return dct

    def __init__(cls, name, bases, attrs, on=[]):
        """Initialize after the class is created, collecting all the case argument
        and function data saved by the `CaseCollectingDict` into a dict."""
        # Evaluate if an `on` argument was passed.
        if on != []: # Note [] is unhashable, so it doesn't collide with a control var.
            cls.switch(on)

    def __call__(cls, control_var, *args, **kwargs):
        """Evaluate the switch for `value` if the class is called as a function."""
        return cls.switch(control_var, *args, **kwargs)


class Switch(metaclass=SwitchMetaclass):
    """The main `Switch` class used to define a case-switch."""
    @classmethod
    def switch(cls, control_var, *args, **kwargs):
        """Activate the switch statement for the given value, returning a tuple of
        all the return function values of any case functions that are executed."""
        return_vals = []
        fundict = cls._fundict
        if (control_var,) in fundict:
            fun_list = fundict[(control_var,)]
            return_vals = [fun(*args, **kwargs) for fun in fun_list]
        elif () in fundict:
            return_vals = [fundict[()](*args, **kwargs)]
        else:
            raise SwitchError("No case matches and no default is defined.")
        return tuple(return_vals)

#
# Exceptions.
#

class SwitchError(Exception):
    pass


