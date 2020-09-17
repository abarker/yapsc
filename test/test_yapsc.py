from yapsc import Switch, case, default, SwitchError

def test_basic_stuff():

    class StringCaseSwitch(Switch, on="salad"):

        @case("egg")
        def _():
            print("case egg")

        @case("salad")
        def _():
            print("case salad")

    StringCaseSwitch("egg") # Runs the function for case "egg".
    StringCaseSwitch("egg") # Runs the function for case "egg".
    StringCaseSwitch.switch("salad") # Runs the function for case "egg".

    print()

    def in_fun():

        class SwitchOn(Switch, on="zooba"):

            @case("water")
            def _():
                print("case water")
                print("local_var =", local_var)
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

def test_cases_returning_values():
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

test_basic_stuff()
test_cases_taking_args_and_kwargs()
test_cases_returning_values()
test_exception()

