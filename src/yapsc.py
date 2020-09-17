"""

Yet Another Python Switch-Case

Test ideas for magic switch statement from a class def.  Inspired by
   https://old.reddit.com/r/Python/comments/irapp9/introducing_switches_a_package_that_adds_support/

Note Python may add a pattern match, which would possibly allow real cases.
   https://www.python.org/dev/peps/pep-0622/

Some projects similar.
   https://github.com/tetrapus/switchcase/blob/master/switchclass.py


Usage notes:

    * Define the switch class in the scope you want to be visible to the defined case
      code.

    * If possible don't define the switch class inside a loop.  Just call `switch` inside
      the loop.  Then in the loop you get real dict-hashed function dispatch without the
      definition overhead.

    * No fallthrough, but the `case` command can take multiple arguments to match (like
      Pascal rather than like C).

    * Only hashable values can be switched on.

    * Calls outside the definition return a list of all the return values of the
      functions that are run.

    * If the case functions take parameters they must all take the same number of parameters
      and the arguments must be passed as extra arguments to the call to the switch.  The
      `on` keyword cannot be used in this case.

    * The class name can be arbitrary, but should be different from any other switches
      in the same scope.  The case function names are ignored and can either be "_" or
      any string not starting with "_" except for "switch".

    * The switch can be called 1) as a function call to the user-defined switch class,
      2) via the `switch` classmethod of the user-defined switch class, or 3) by passing
      the value and any arguments to the `on` keyword parameter to the switch class
      definition.

"""

from collections import defaultdict
from types import SimpleNamespace

#
# Utility classes.
#

class CaseCollectingDict(dict):
    """This is a dict superclass which adds the feature of saving the data
    passed to `__setitem__` calls for the key `_` to a dict.  It is set as the
    `__prepare__` method `SwitchMetaclass`."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["_fundict"] = defaultdict(list) # Non-string key: avoid clashes with attr names.

    def __setitem__(self, key, value):
        if isinstance(key, str) and isinstance(value, list) and key != "switch" and (
                                                                key == "_" or key[0] != "_"):
            fun, case_args = value
            if not case_args:
                self["_fundict"][()] = fun
            for arg in case_args:
                # Wrap `arg` in a tuple so the default case can have a unique `()` key.
                self["_fundict"][(arg,)].append(fun)
        else:
            super().__setitem__(key, value)

#
# Decorator functions.
#

def case(*args):
    """The `case` decorator used in switch definitions."""
    def process_case(fun):
        return [fun, args]
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
        if on != []: # Note [] is unhashable, so it cannot conflict with values.
            cls.switch(on)

    def __call__(cls, value, *args, **kwargs):
        """Evaluate the switch for `value` if the class is called as a function."""
        return cls.switch(value, *args, **kwargs)


class Switch(metaclass=SwitchMetaclass):
    """The main `Switch` class used to define a case-switch."""
    @classmethod
    def switch(cls, val, *args, **kwargs):
        """Activate the switch statement for the given value, returning a tuple of
        all the return function values of any case functions that are executed."""
        return_vals = []
        fundict = cls._fundict
        if (val,) in fundict:
            fun_list = fundict[(val,)]
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


