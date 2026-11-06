import re

import sympy as sp


X = sp.Symbol(
    "x"
)


ALLOWED_MATH_PATTERN = (
    re.compile(
        r"^[0-9xX+\-*/().^=\s]+$"
    )
)


SUBSTITUTION_PATTERN = (
    re.compile(
        (
            r"^\s*"
            r"(?:y\s*=\s*)?"
            r"(?P<expression>.+?)"
            r"\s+when\s+"
            r"x\s*=\s*"
            r"(?P<value>"
            r"-?\d+(?:\.\d+)?"
            r"(?:/\d+(?:\.\d+)?)?"
            r")"
            r"\s*$"
        ),

        re.IGNORECASE,
    )
)


def normalize_math_text(
    text: str,
) -> str:

    cleaned = (
        text
        .strip()
        .replace(
            "X",
            "x",
        )
        .replace(
            "^",
            "**",
        )
        .replace(
            "×",
            "*",
        )
        .replace(
            "÷",
            "/",
        )
    )


    if (
        not cleaned
    ):

        raise ValueError(
            "Math expression is empty."
        )


    if (
        not ALLOWED_MATH_PATTERN
        .fullmatch(
            cleaned
        )
    ):

        raise ValueError(
            "Unsupported characters "
            "in Math expression."
        )


    # 3x -> 3*x

    cleaned = re.sub(
        r"(?<=\d)(?=x)",

        "*",

        cleaned,
    )


    # 2(x + 1) -> 2*(x + 1)

    cleaned = re.sub(
        r"(?<=\d)(?=\()",

        "*",

        cleaned,
    )


    # x(x + 1) -> x*(x + 1)

    cleaned = re.sub(
        r"(?<=x)(?=\()",

        "*",

        cleaned,
    )


    # (x + 1)2 -> (x + 1)*2

    cleaned = re.sub(
        r"(?<=\))(?=[x\d(])",

        "*",

        cleaned,
    )


    return cleaned


def parse_expression(
    text: str,
):

    normalized = (
        normalize_math_text(
            text
        )
    )


    if (
        "="
        in normalized
    ):

        raise ValueError(
            "Expected an expression, "
            "not an equation."
        )


    return (
        sp.sympify(
            normalized,

            locals={
                "x":
                    X,
            },
        )
    )


def parse_equation(
    text: str,
) -> sp.Eq:

    normalized = (
        normalize_math_text(
            text
        )
    )


    if (
        normalized.count(
            "="
        )
        != 1
    ):

        raise ValueError(
            "Expected exactly one "
            "'=' sign."
        )


    left_text, right_text = (
        normalized.split(
            "="
        )
    )


    left = (
        sp.sympify(
            left_text,

            locals={
                "x":
                    X,
            },
        )
    )


    right = (
        sp.sympify(
            right_text,

            locals={
                "x":
                    X,
            },
        )
    )


    return (
        sp.Eq(
            left,
            right,
            evaluate=False,
        )
    )


def solve_linear_equation(
    text: str,
):

    equation = (
        parse_equation(
            text
        )
    )


    solutions = (
        sp.solve(
            equation,
            X,
        )
    )


    if (
        len(
            solutions
        )
        != 1
    ):

        raise ValueError(
            "Only single-solution "
            "linear equations "
            "are supported."
        )


    solution = (
        sp.simplify(
            solutions[0]
        )
    )


    if (
        solution.has(
            X
        )
    ):

        raise ValueError(
            "Could not isolate x."
        )


    return solution


def evaluate_arithmetic(
    text: str,
):

    expression = (
        parse_expression(
            text
        )
    )


    if (
        expression
        .free_symbols
    ):

        raise ValueError(
            "Arithmetic expression "
            "contains an unknown "
            "variable."
        )


    return (
        sp.simplify(
            expression
        )
    )


# ======================================================
# Phase 19 substitution
#
# Examples:
#
# 3x + 2 when x = 4
# y = 2x + 3 when x = 5
# ======================================================

def evaluate_substitution_problem(
    text: str,
):

    match = (
        SUBSTITUTION_PATTERN
        .match(
            text
        )
    )


    if (
        match is None
    ):

        raise ValueError(
            "Unsupported substitution "
            "problem format."
        )


    expression_text = (
        match.group(
            "expression"
        )
        .strip()
    )


    value_text = (
        match.group(
            "value"
        )
    )


    expression = (
        parse_expression(
            expression_text
        )
    )


    if (
        expression.free_symbols
        - {
            X
        }
    ):

        raise ValueError(
            "Only x is supported "
            "as a variable."
        )


    x_value = (
        sp.sympify(
            value_text
        )
    )


    result = (
        sp.simplify(
            expression.subs(
                X,
                x_value,
            )
        )
    )


    if (
        result.free_symbols
    ):

        raise ValueError(
            "Substitution did not "
            "produce a number."
        )


    return result


def extract_equation_candidates(
    message: str,
) -> list[
    str
]:

    parts = (
        re.split(
            r"[;\n]+",
            message,
        )
    )


    candidates: list[
        str
    ] = []


    equation_pattern = (
        re.compile(
            (
                r"([0-9xX+\-*/().^\s]+"
                r"="
                r"[0-9xX+\-*/().^\s]+)"
            )
        )
    )


    for part in (
        parts
    ):

        matches = (
            equation_pattern
            .findall(
                part
            )
        )


        for match in (
            matches
        ):

            cleaned = (
                match
                .strip()
                .rstrip(
                    " ."
                )
            )


            if (
                cleaned
            ):

                candidates.append(
                    cleaned
                )


    return candidates


def extract_isolated_x_answer(
    text: str,
):

    normalized = (
        text
        .strip()
        .replace(
            "X",
            "x",
        )
    )


    patterns = [

        (
            r"\bx\s*=\s*"
            r"(-?\d+(?:\.\d+)?"
            r"(?:/\d+(?:\.\d+)?)?)"
        ),

        (
            r"(-?\d+(?:\.\d+)?"
            r"(?:/\d+(?:\.\d+)?)?)"
            r"\s*=\s*x\b"
        ),
    ]


    for pattern in (
        patterns
    ):

        match = re.search(
            pattern,
            normalized,
        )


        if (
            match
        ):

            return (
                sp.sympify(
                    match.group(
                        1
                    )
                )
            )


    return None


def extract_numeric_answer(
    message: str,
):

    number_pattern = (
        re.compile(
            (
                r"-?\d+(?:\.\d+)?"
                r"(?:/\d+(?:\.\d+)?)?"
            )
        )
    )


    matches = (
        number_pattern
        .findall(
            message
        )
    )


    if (
        not matches
    ):

        return None


    return (
        sp.sympify(
            matches[-1]
        )
    )


def values_equal(
    first,
    second,
) -> bool:

    try:

        difference = (
            sp.simplify(
                first
                - second
            )
        )


        return bool(
            difference == 0
        )


    except Exception:

        return False


def format_math_value(
    value,
) -> str:

    return str(
        sp.simplify(
            value
        )
    )