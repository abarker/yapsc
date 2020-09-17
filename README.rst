.. default-role:: code

yapsc -- Yet Another Python Switch-Case
=======================================

This is another Python implementation of a switch-case statement.  Many
versions and variations of Python switch-case implementations are out there,
but I think this one has some advantages over the ones I've seen.  (The closest
to this version is probably at `tetrapus/switchcase
<https://github.com/tetrapus/switchcase>`_.)

This is basically a nice syntax for wrapping a dict-based function dispatch.
The switch call is quite efficient, and can be separated from the switch
definition and its associated overhead.  Fallthrough is not implemented, but
the `case` command can take multiple arguments to match (like Pascal's case
statement rather than C's).

Example code
------------

.. code-block:: python

   from yapsc import Switch, case, default

   class CommandSwitch(Switch):

       @case("play")
       def _():
           print("play command")

       @case("back")
       def _():
           print("back command")

       @case("forward")
       def _():
           print("forward command")

       @case("back", "forward")
       def _():
           print("back or forward command")

       @case # Default.
       def _():
           print("default case")

   command = "back"
   CommandSwitch(command)

This prints out::

   back command
   back or forward command

Usage notes
-----------

Usage notes:

   * Any (and only) hashable values can be switched on.

   * When there are multiple matching cases their function are called in the
     sequence that they were defined in.

   * The class name can be arbitrary, but should be different from any other
     switches in the same scope.  The case-function names are ignored and can
     either be "_" or a valid attribute name not starting with "_", excepting
     "switch".

   * The switch can be called 1) as a function call to the user-defined switch
     class, 2) via the `switch` classmethod of the user-defined switch class,
     or 3) by passing the value as the `on` keyword argument to the switch
     class definition.

   * Calls to the switch return a tuple of all the return values of all the
     case-functions that were run.  (But running from the `on` keyword in the
     switch definition does not return a value.)

   * The switch class should be defined in the scope you want to be visible to
     the case-function code.

   * If possible don't define the switch class inside a loop; just put the call
     inside the loop.  Then in the loop you get real dict-hashed function
     dispatch without the definition overhead.

   * If the case-functions take parameters they must all take the same number
     of parameters.  The arguments must be passed as extra arguments in the
     call to the switch.  The `on` keyword cannot be used in this case.

It should be noted that if Python's `PEP-622
<https://www.python.org/dev/peps/pep-0622/>`_ for pattern matching is accepted
then for future Python versions these switch-case implementations will become
pointless.

Installation
------------

.. code-block:: bash

   pip install yapsc

