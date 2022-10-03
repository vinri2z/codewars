from math_expr import calc


def run_tests(expr: str):
    assert calc(expr) == eval(expr), f"{expr} != {calc(expr)}"


def test_calc():
    run_tests("3 -(-1)")
    run_tests(" -(-34)")
    run_tests("    -(-34)")
    run_tests("-(-34)")
    run_tests("6 / -(45 - 90)")
    run_tests("(-34)")
    run_tests("6 / (45 - 90)")
    run_tests("3 - (-1)")
    run_tests("(1728 - 19281) / -(-8938 - 19129 - (-738))")
    run_tests("-(-17) - (-85 * -31 + (20)) * (-65 / -(((-(33 - -44)))) - 34)")
    run_tests("-(-88) * (-13 * 62 + -(10)) - (65 * (((-(-1 + -72)))) - -94)")
