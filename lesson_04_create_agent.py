
import os

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from read_env import (
    api_key,
    model_name,
    base_url)

@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。"""
    return a * b


def main():

    if not api_key:
        raise RuntimeError("请先设置 OPENAI_API_KEY")

    if not model_name:
        raise RuntimeError("请先设置 OPENAI_MODEL")

    model_kwargs = {
        "model": model_name,
        "api_key": api_key,
        "temperature": 0,
    }

    if base_url:
        model_kwargs["base_url"] = base_url

    model = ChatOpenAI(**model_kwargs)

    agent = create_agent(
        model=model,
        tools=[multiply],
        system_prompt=(
            "你是一名严谨的数学助手。"
            "涉及乘法计算时，优先使用提供的乘法工具。"
            "根据工具返回的结果回答，不要编造计算结果。"
        ),
    )

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "请使用工具计算 237 × 419，并解释结果。",
            }
        ]
    })

    # Agent 返回的是状态字典，其中包含消息列表
    for index, message in enumerate(result["messages"]):
        print(f"\n--- 消息 {index + 1} ---")
        print("类型：", type(message).__name__)
        print("内容：", message.content)

        if getattr(message, "tool_calls", None):
            print("工具调用：", message.tool_calls)

    print("\n最终回答：")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
