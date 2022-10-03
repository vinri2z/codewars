import re

# regex matching a number (possibly float, possibly negative and
# possibly in scientific expression
NUMBER = r"-?\d+(\.\d*(e[+-]\d+)?)?"

# regex matching any classic mathematical operation
OP = r"[\/*+-]"


def calc_pair(mtch: re.Match):
    """Given the match of an operation (number_1 operation number_2) returns the result of the operation as a float number
    :param mtch: regex match of an operation with 2 arguments
    :return: result of the operation as a float"""
    n_1, n_2, op = float(mtch.group('n_1')), float(mtch.group('n_2')), mtch.group('op')
    if op == '/':
        result = n_1 / n_2
    elif op == '*':
        result = n_1 * n_2
    elif op == '+':
        result = n_1 + n_2
    elif op == '-':
        result = n_1 - n_2
    else:
        raise ValueError("Couldn't parse expr")
    return str(result)


def solve_no_par(expression: str) -> str:
    """Calculates the value of a mathematical expression that does not contain parentheses using classical
    operation priority
    :param expression: mathematical expression to be calculated
    :return: the string expression calculated (should be a float)"""
    for ops in ('/*', '+-'):
        reg = fr"(?P<n_1>{NUMBER}) *(?P<op>[{ops}]) *(?P<n_2>{NUMBER})"
        while re.search(reg, expression):
            expression = re.sub(reg, calc_pair, expression, count=1)
    return expression


def is_float(element: str) -> bool:
    """
    Checks if a string expression can directly be converted to float
    :param element: mathematical expression
    :return: True if element is a valid float as a string else returns False"""
    try:
        float(element)
        return True
    except ValueError:
        return False


def replace_parentheses(mtch: re.Match) -> str:
    """Replaces an expression between parentheses (and possibly a - sign in front of it) by its equivalent value
    :param mtch: the regex match object matching the minus sign and parentheses"""
    par_exp = calc(mtch.group('par_exp'))
    return (mtch.group('prev') or '') + (str(-par_exp) if mtch.group('min') else str(par_exp))


def solve_inside_par(expression: str) -> str:
    """Detects parentheses and calculates the expression inside with a change of sign in case there is a -
    sign in front of the parenthesis and no number precedes that sign
    :param expression: mathematical expression to be calculated
    """
    minus = fr"((?P<min>(?P<prev>({OP}|\A) *)-))?"
    par_search = fr"{minus}\((?P<par_exp>({NUMBER}|{OP}| )*)\)"

    while re.search(par_search, expression):
        expression = re.sub(par_search, replace_parentheses, expression, count=1)
    return expression


def count_signs(mtch: re.Match) -> str:
    """Return the equivalent sign to a match of multiple consecutive +- signs
    :param mtch: matching a sequence of +- signs
    :return: + or - depending on the parity of - signs"""
    return ('+', '-')[mtch.group().count('-') % 2]


def simplify_signs(expression: str) -> str:
    """Simplifies an expression by replacing any sequence of consecutive +- signs by its equivalent in one sign
    :param expression: mathematical expression to be simplified
    :return: the expression after simplifying every sequence of 2 or more + or - signs"""
    return re.sub(r"[+-]{2,}", count_signs, expression)


def calc(expression: str) -> float:
    """Calculates a mathematical expression as a calculator would
    :param expression: mathematical expression to be calculated
    :return: the result equivalent to do calculating the expression
    """
    if is_float(expression):
        return float(expression)
    expression = solve_inside_par(expression.strip())
    expression = simplify_signs(expression)
    expression = solve_no_par(expression)
    return calc(expression)
