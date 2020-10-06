"""

Yet Another Python Switch-Case


"""

from collections import defaultdict

DUPS_DEFAULT = False # The default for allowing duplicate case values.

#
# Utility classes.
#

_marker = "Unique element to detect error conditions."

class CaseCollectingDict(dict):
    """This is a dict subclass which adds the feature of saving the data
    passed to `__setitem__` calls for certain key values.  It is set as the
    `__prepare__` method `SwitchMetaclass`."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["_fundict"] = defaultdict(list) # Non-string key: avoid clashes with attr names.

    def __setitem__(self, key, value):
        if hasattr(value, "_yapsc_id") and value._yapsc_id is _marker:
            raise SwitchError("The 'case' decorator was called with no arguments."
                              " Use the '@default' decorator for the default case.")

        if isinstance(key, str) and isinstance(value, list) and (
                                               len(value) == 3 and value[2] is _marker):
            # Got a list of data from the `case` or `default` decorator.
            if key != "switch" and (key == "_" or key[0] != "_"):
                fun, case_args, _mark = value
                if not case_args: # Data from from the `default` decorator.
                    if () in self["_fundict"]:
                        raise SwitchError("Multiple instances of default decorator.")
                    self["_fundict"][()] = [fun] # In a list for consistency.
                for arg in case_args: # Data from the `case` decorator.
                    # Wrap `arg` in a tuple so the default case can have a unique `()` key.
                    fun_list = self["_fundict"][(arg,)]
                    if len(fun_list) == 1 and not self["_allow_dups"]:
                        raise SwitchError("Duplicate use of case value '{}'".format(arg))
                    fun_list.append(fun)
                super().__setitem__(key, staticmethod(fun)) # Set the fun as a staticmethod.
            else:
                raise SwitchError("Decorator called with a disallowed case name.")

        else: # Allow arbitrary attrs to be set, but ignore them as part of the switch.
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
        return [fun, case_values, _marker]
    process_case._yapsc_id = _marker # To detect when `case` is called with no parens.
    return process_case

def default(fun):
    """The `default` decorator used in switch definitions."""
    return [fun, [], _marker]

#
# The `Switch` metaclass and class.
#

class SwitchMetaclass(type):
    """Metaclass for the `Switch` class."""
    def __new__(mcs, name, bases, attrs, *, on=[], dups=DUPS_DEFAULT):
        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class

    @classmethod
    def __prepare__(mcs, name, bases, on=[], dups=DUPS_DEFAULT):
        """Return the dict-like object to be set as `__dict__` (i.e., to hold
        the class attributes)."""
        dct = CaseCollectingDict() # Saves data each time a case is defined.
        dct["_allow_dups"] = dups # Needs to be available during class creation.
        return dct

    def __init__(cls, name, bases, attrs, on=[], dups=DUPS_DEFAULT):
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
            return_vals = [fundict[()][0](*args, **kwargs)]
        else:
            raise SwitchError("No case matches and no default is defined.")
        if cls._allow_dups:
            return tuple(return_vals)
        else:
            return return_vals[0]

#
# Exceptions.
#

class SwitchError(Exception):
    pass


