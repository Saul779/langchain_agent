
#第二部分
from langchain_core.tools import tool, ToolException

@tool
def safe_divide_for_agent(a: float, b: float) -> float:
    """计算 a 除以 b。除数不能为零。"""
    if b == 0:
        raise ToolException("除数不能为零。")
    return a / b

# 在创建工具对象后设置异常处理策略
safe_divide_for_agent.handle_tool_error = "计算失败：请检查参数，并确保除数不为零。"


if __name__ == '__main__':
    safe_divide_for_agent.invoke({"a": 10, "b": 2})

# 第一部分
from langchain_core.tools import tool, ToolException
@tool
def safe_divide(a: float, b: float) -> float:
    """计算 a 除以 b。除数不能为零。"""

    if b == 0:
        raise ToolException("除数不能为零，请提供非零的除数。")
    return a / b

# 测试正常情况
print(safe_divide.invoke({"a": 10, "b": 2}))

# 测试异常情况
try:
    print(safe_divide.invoke({"a": 10, "b": 0}))
except ToolException as exc:
    print("捕获到工具异常：", exc)



