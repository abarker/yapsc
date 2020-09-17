from yapsc import Switch, case, default, SwitchError

def test_basic_stuff():

    class StringCaseSwitch(Switch, on="salad"):

        @case("egg")
        def _():
            print("case egg")
            return "egg"

        @case("salad")
        def _():
            print("case salad")
            return "salad"

    assert StringCaseSwitch("egg") == ("egg",)
    assert StringCaseSwitch("egg") == ("egg",)
    assert StringCaseSwitch.switch("salad") == ("salad",)

    print()

    def in_fun():

        class SwitchOn(Switch, on="zooba"):

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

    in_fun()

def test_cases_taking_args_and_kwargs():
    # TODO
    pass

def test_exception():

    class StringCaseSwitch(Switch, on="egg"):

        @case("egg")
        def _():
            print("case egg")

    try: # Raise an exception.
        StringCaseSwitch.switch("zzz")
        assert False
    except SwitchError:
        assert True

def test_example_code():

    class CommandSwitch(Switch):

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


test_basic_stuff()
test_cases_taking_args_and_kwargs()
test_exception()
test_example_code()
