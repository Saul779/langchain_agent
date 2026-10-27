from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。"""
    return a * b


def test_mock_model_tool_call():
    # 第一次模型响应：要求调用 multiply 工具
    model_response = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "multiply",
                "args": {"a": 6, "b": 7},
                "id": "call_001",
                "type": "tool_call",
            }
        ],
    )

    # 检查模型是否请求了正确的工具
    assert len(model_response.tool_calls) == 1

    tool_call = model_response.tool_calls[0]
    assert tool_call["name"] == "multiply"
    assert tool_call["args"] == {"a": 6, "b": 7}

    # 执行工具
    result = multiply.invoke(tool_call["args"])
    assert result == 42

    # 模拟第二次模型响应
    final_response = AIMessage(content="计算结果是 42")
    assert final_response.content == "计算结果是 42"


if __name__ == "__main__":
    test_mock_model_tool_call()
    print("Mock 模型工具调用测试通过")