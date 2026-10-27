
from langchain_core.tools import tool, ToolException


def multiply(a: int, b: int) -> int:
    """纯 Python 乘法逻辑。"""
    return a * b


@tool
def multiply_tool(a: int, b: int) -> int:
    """计算两个整数的乘积。"""
    return multiply(a, b)


@tool
def safe_divide(a: float, b: float) -> float:
    """计算 a 除以 b，除数不能为零。"""
    if b == 0:
        raise ToolException("除数不能为零")

    return a / b
