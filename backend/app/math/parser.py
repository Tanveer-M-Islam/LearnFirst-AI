import re

import sympy as sp


X = sp.Symbol("x")


ALLOWED_MATH_PATTERN = re.compile(
    r"^[0-9xX+\-*/().^=\s]+$"
)


def normalize_math_text(
    text: str,
) -> str:
    """
    Clean a small supported subset of Math.

    Example:
        3x + 5 = 20
    becomes:
        3*x + 5 = 20
    """

    cleaned = (
        text
        .strip()
        .replace("X", "x")
        .replace("^", "**")
    )

    if not cleaned:
        raise ValueError(
            "Math expression is empty."
        )

    if not ALLOWED_MATH_PATTERN.fullmatch(
        cleaned
    ):
        raise ValueError(
            "Unsupported characters in "
            "Math expression."
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
    normalized = normalize_math_text(
        text
    )

    if "=" in normalized:
        raise ValueError(
            "Expected an expression, "
            "not an equation."
        )

    return sp.sympify(
        normalized,
        locals={
            "x": X,
        },
    )


def parse_equation(
    text: str,
) -> sp.Eq:

    normalized = normalize_math_text(
        text
    )

    if normalized.count("=") != 1:
        raise ValueError(
            "Expected exactly one '=' sign."
        )

    left_text, right_text = (
        normalized.split("=")
    )

    left = sp.sympify(
        left_text,
        locals={
            "x": X,
        },
    )

    right = sp.sympify(
        right_text,
        locals={
            "x": X,
        },
    )

    return sp.Eq(
        left,
        right,
        evaluate=False,
    )


def solve_linear_equation(
    text: str,
):
    equation = parse_equation(
        text
    )

    solutions = sp.solve(
        equation,
        X,
    )

    if len(solutions) != 1:
        raise ValueError(
            "Only single-solution linear "
            "equations are supported."
        )

    solution = sp.simplify(
        solutions[0]
    )

    if solution.has(X):
        raise ValueError(
            "Could not isolate x."
        )

    return solution


def evaluate_arithmetic(
    text: str,
):
    expression = parse_expression(
        text
    )

    if expression.free_symbols:
        raise ValueError(
            "Arithmetic expression contains "
            "an unknown variable."
        )

    return sp.simplify(
        expression
    )


def extract_equation_candidates(
    message: str,
) -> list[str]:
    """
    Extract equations from a student's message.

    Example:

        3x = 12; x = 12

    returns:

        [
            "3x = 12",
            "x = 12"
        ]
    """

    parts = re.split(
        r"[;\n]+",
        message,
    )

    candidates: list[str] = []

    equation_pattern = re.compile(
        r"([0-9xX+\-*/().^\s]+"
        r"="
        r"[0-9xX+\-*/().^\s]+)"
    )

    for part in parts:

        matches = (
            equation_pattern.findall(
                part
            )
        )

        for match in matches:

            cleaned = (
                match
                .strip()
                .rstrip(" .")
            )

            if cleaned:
                candidates.append(
                    cleaned
                )

    return candidates


def extract_isolated_x_answer(
    text: str,
):
    """
    Detect answers like:

        x = 5
        5 = x
        x = -2
        x = 3/4
    """

    normalized = (
        text
        .strip()
        .replace("X", "x")
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

    for pattern in patterns:

        match = re.search(
            pattern,
            normalized,
        )

        if match:

            value_text = (
                match.group(1)
            )

            return sp.sympify(
                value_text
            )

    return None


def extract_numeric_answer(
    message: str,
):
    """
    Extract the final numerical value appearing
    in a simple arithmetic response.
    """

    number_pattern = re.compile(
        r"-?\d+(?:\.\d+)?"
        r"(?:/\d+(?:\.\d+)?)?"
    )

    matches = number_pattern.findall(
        message
    )

    if not matches:
        return None

    return sp.sympify(
        matches[-1]
    )


def values_equal(
    first,
    second,
) -> bool:

    try:

        difference = sp.simplify(
            first - second
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
        sp.simplify(value)
    )