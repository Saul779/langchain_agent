
import pytest
from langchain_core.tools import ToolException
from lesson_07_tools import multiply, multiply_tool, safe_divide


def test_multiply():
    assert multiply(237, 419) == 99303


def test_multiply_zero():
    assert multiply(100, 0) == 0


def test_multiply_negative():
    assert multiply(-3, 4) == -12


def test_multiply_tool():
    result = multiply_tool.invoke({"a": 237, "b": 419})
    assert result == 99303


def test_safe_divide():
    result = safe_divide.invoke({"a": 10, "b": 2})
    assert result == 5


def test_safe_divide_by_zero():
    with pytest.raises(ToolException):
        safe_divide.invoke({"a": 10, "b": 0})


import pytest
from lesson_07_tools import multiply


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (0, 100, 0),
        (-3, 4, -12),
        (237, 419, 99303),
    ],
)
def test_multiply_cases(a, b, expected):
    assert multiply(a, b) == expected