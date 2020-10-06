from yapsc import Switch, case, default, SwitchError

def test_basic_stuff():

    class StringCaseSwitch(Switch, dups=True, on="salad"):

        @case("egg")
        def _():
            print("case egg")
            return "egg"

        @case("salad")
        def _():
            print("case salad")
            return "salad"

        @case(99) # Test non-string.
        def _():
            print("case int 99")
            return "99"

    assert StringCaseSwitch("egg") == ("egg",)
    assert StringCaseSwitch("egg") == ("egg",)
    assert StringCaseSwitch.switch("salad") == ("salad",)
    assert StringCaseSwitch(99) == ("99",)

    print()

    def in_fun():

        class SwitchOn(Switch, dups=True, on="zooba"):

            @case("water")
            def _():
                print("case water")
                assert local_var == "local"
                return "water"

            @case("salad")
            def _():
                print("case salad")

            @case("water", "salad")
            def anyname():
                print("case water or salad")
                return "water or salad"

            @default
            def _():
                print("default case")
                return "default"

        local_var = "local"

        for possibly_long_loop in [0]:
            value = SwitchOn("water")
            assert value == ("water", "water or salad")
            SwitchOn.switch("salad")
            value = SwitchOn.switch("should be default")
            assert value == ("default",)

        # Test running a case function as a staticmethod.
        value = SwitchOn.anyname()
        assert value == "water or salad"

    in_fun()

def test_cases_taking_args_and_kwargs():

    class CommandSwitch(Switch, dups=True):

        @case("play")
        def _(param, *, kw):
            assert param == 99
            assert kw == "kw"
            print("play command")
            return "play"

        @case("back")
        def _(param, **kwargs):
            assert param == 99
            print("back command")
            return "back"

        @case("forward")
        def _(param, *, kw2=4):
            assert param == 99
            assert kw2 == "kw2"
            print("forward command")
            return "forward"

        @case("back", "forward")
        def _(param, **kwargs):
            assert param == 99
            print("back or forward command")
            return "back or forward"

        @default # Default.
        def _(param, **kwargs):
            assert param == 99
            print("default case")
            return "default"

    command = "back"
    output = CommandSwitch(command, 99, kw="kw", kw2="kw2")
    assert output == ("back", "back or forward")
    output = CommandSwitch("non-command", 99, kw="kw", kw2="kw2")
    assert output == ("default",)


def test_exceptions():

    class StringCaseSwitch(Switch, dups=True, on="egg"):

        @case("egg")
        def _():
            print("case egg")

    # Exception no case matches but no default case.
    try:
        StringCaseSwitch.switch("zzz")
        assert False
    except SwitchError:
        assert True

    # Exception where case decorator is called with no parens.
    try:
        class BadSwitchEmptyCase(Switch, dups=True):
            @case
            def _():
                pass
        assert False
    except SwitchError:
        assert True

    # Exception multiple @default decorators.
    try:
        class MultipleDefault(Switch, dups=True):
            @default
            def _():
                pass
            @default
            def _():
                pass
        assert False
    except SwitchError:
        assert True

    # Exception dups not allowed but dups present.
    # NOTE: Exceptions on dups is now the default behavior.
    try:
        class ForbiddenDups(Switch, dups=False):
            @case("a")
            def _():
                pass
            @case("b","a")
            def _():
                pass
        assert False
    except SwitchError:
        assert True

    # Exception where the case function is given a disallowed name (switch here
    # would clash with the classmethod).
    try:
        class BadCaseName(Switch, dups=True):
            @case("x")
            def switch():
                pass
        assert False
    except SwitchError:
        assert True

    # Make sure arbitrary attrs can still be added after checking for above error
    # conditions.
    class AttrAdd(Switch, dups=True):
        @case("x")
        def _():
            pass

        x = [1,2,3] # Make sure arbitrary attrs can be added.

    AttrAdd.y = [4,5,6]
    assert AttrAdd.x == [1,2,3]
    assert AttrAdd.y == [4,5,6]

def test_old_example_code():

    class CommandSwitch(Switch, dups=True):

        @case("play")
        def _():
            print("play command")
            return "play"

        @case("back")
        def _():
            print("back command")
            return "back"

        @case("forward")
        def _():
            print("forward command")
            return "forward"

        @case("back", "forward")
        def _():
            print("back or forward command")
            return "back or forward"

        @default # Default.
        def _():
            print("default case")
            return "default"

    command = "back"
    output = CommandSwitch(command)
    assert output == ("back", "back or forward")
    output = CommandSwitch("non-command")
    assert output == ("default",)

def test_example_code():
   """Test new example code, after the default was changed to disallow dups by default."""

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


test_basic_stuff()
test_cases_taking_args_and_kwargs()
test_exceptions()
test_old_example_code()
test_example_code()

