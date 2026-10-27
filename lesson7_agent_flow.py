from unittest.mock import Mock
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。"""
    return a * b


def run_tool_call_flow(model, question: str) -> str:
    # 第一次模型调用
    response = model.invoke([HumanMessage(content=question)])

    if not response.tool_calls:
        return str(response.content)

    # 执行模型请求的工具
    tool_messages = []

    for tool_call in response.tool_calls:
        if tool_call["name"] != "multiply":
            raise ValueError(f"未知工具：{tool_call['name']}")

        result = multiply.invoke(tool_call["args"])

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )

    # 将原问题、工具调用请求和工具结果交给模型
    second_response = model.invoke(
        [
            HumanMessage(content=question),
            response,
            *tool_messages,
        ]
    )

    return str(second_response.content)


def test_agent_tool_call_flow():
    # 第一次响应：模型要求执行 multiply(6, 7)
    tool_call_response = AIMessage(
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

    # 第二次响应：模型给出最终答案
    final_response = AIMessage(content="42")

    fake_model = Mock()
    # 序列式返回列表中的值，每次调用取一个
    fake_model.invoke.side_effect = [
        tool_call_response,
        final_response,
    ]

    result = run_tool_call_flow(fake_model, "计算 6 * 7")

    assert result == "42"
    assert fake_model.invoke.call_count == 2

    # 验证第二次调用确实包含工具结果,获取第二次调用invoke时传入的参数
    second_messages = fake_model.invoke.call_args_list[1].args[0]
    print(second_messages)
    print(fake_model.invoke.call_args_list)

    tool_messages = [
        message
        for message in second_messages
        if isinstance(message, ToolMessage)
    ]

    assert len(tool_messages) == 1
    assert tool_messages[0].content == "42"
    assert tool_messages[0].tool_call_id == "call_001"


if __name__ == "__main__":
    test_agent_tool_call_flow()
    print("Agent 工具调用流程测试通过")


def test_agent_rejects_unknown_tool():
    unknown_tool_response = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "delete_database",
                "args": {},
                "id": "call_unknown",
                "type": "tool_call",
            }
        ],
    )

    fake_model = Mock()
    fake_model.invoke.return_value = unknown_tool_response

    try:
        run_tool_call_flow(fake_model, "执行操作")
    except ValueError as exc:
        assert "未知工具" in str(exc)
    else:
        raise AssertionError("预期抛出 ValueError，但没有抛出")


import pytest


def test_agent_rejects_unknown_tool_with_pytest():
    unknown_tool_response = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "delete_database",
                "args": {},
                "id": "call_unknown",
                "type": "tool_call",
            }
        ],
    )

    fake_model = Mock()
    fake_model.invoke.return_value = unknown_tool_response

    with pytest.raises(ValueError, match="未知工具"):
        run_tool_call_flow(fake_model, "执行操作")