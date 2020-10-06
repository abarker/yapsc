.. default-role:: code

yapsc -- Yet Another Python Switch-Case
=======================================

Another Python implementation of a switch-case statement.  Many versions and
variations of Python switch-case constructs are out there, but this one has
syntax and a combination of features I have not seen.  (The closest to this
version is probably at `tetrapus/switchcase
<https://github.com/tetrapus/switchcase>`_.)

This is basically just convenient syntax for defining a dict-based function
dispatch.  The switch call is quite efficient, and can be separated from the
switch definition and its associated overhead.  Fallthrough is not implemented,
but the `case` decorator can take multiple arguments to match (like Pascal's
case statement rather than C's).

**Update:** The new default is to raise an exception on a repeated case, which
is more like the Pascal case statement.  Since at most one function can run,
the return value of the case statement is not wrapped in a tuple.  (To get the
previous behavior, with repeats allowed, all matching cases run sequentially,
and the results returned in a tuple, pass the ``dups=True`` flag to the switch
initializer.)

Example code
------------

.. code-block:: python

   from yapsc import Switch, case, default

   class CommandSwitch(Switch):

       @case("play")
       def _():
           print("play command")
           return "play command"

       @case("back")
       def _():
           print("back command")
           return "back command"

       @case("forward")
       def _():
           print("forward command")
           return "forward command"

       @case("exit", "quit")
       def _():
           print("exit or quit command")
           return "exit or quit command"

       @default
       def _():
           print("default case")
           return "default case"

   command = "exit"
   value = CommandSwitch(command)
   assert value == "exit or quit command"

   command = "play"
   value = CommandSwitch(command)
   assert value == "play command"


This prints out::

   exit or quit command

Installation
------------

.. code-block:: bash

   pip install yapsc

Usage notes
-----------

* Any (and only) hashable values can be switched on.  By default a particular
  case value can only appear once in the statement or else an exception is
  raised.

* The class name can be arbitrary, but should be different from any other
  switches in the same scope.
  
* The case-function names are ignored and can either be `"_"` or any valid
  attribute name not starting with `"_"`, excepting `"switch"`.  Case functions
  are set as staticmethods of the class and can also be called that way
  (assuming they have a unique function name).

* The switch can be called 1) as a function call to the user-defined switch
  class, 2) via the `switch` classmethod of the user-defined switch class, or
  3) by passing the control variable as the `on` keyword argument to the switch
  class definition (i.e., passed just after the `Switch`).

* Calls to the switch return the return value of the case-function that was
  run.  (But note that running from the `on` keyword in the switch definition
  does not return a value.)

* The switch class should be defined in the scope you want to be visible to
  the case-function code.

* If possible don't define the switch class inside a loop; just put the call
  inside the loop.  Then in the loop you get real dict-hashed function
  dispatch without the definition overhead.

* If the case-functions take parameters and/or keyword arguments they must
  all take the same number of parameters and same keywords.  The parameter
  values must be passed as extra arguments in the call to the switch.  The
  `on` keyword cannot be used in this case.

* To allow duplicate case values you can pass `dups=True` as a keyword argument
  to the switch class definition (i.e., pass it after the `Switch`
  inheritance).  When there are multiple matching cases their function are
  called in the sequence that they were defined in.  The return value of the
  switch is a tuple of all the return values for each case that was run.

It should be noted that if Python's `PEP-634
<https://www.python.org/dev/peps/pep-0634/>`_ for pattern matching is accepted
then for future Python versions these kinds of switch-case implementations may
become outdated.

