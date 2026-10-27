
import os

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage
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

    if not api_key or not model_name:
        raise RuntimeError(
            "请先设置 OPENAI_API_KEY 和 OPENAI_MODEL"
        )

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
            "计算乘法时优先使用 multiply 工具。"
        ),
    )

    inputs = {
        "messages": [
            {
                "role": "user",
                "content": "请使用工具计算 237 × 419。",
            }
        ]
    }

    print("开始执行 Agent...\n")

    for chunk in agent.stream(
        inputs,
        stream_mode="updates",
    ):
        # 每个 chunk 通常包含一个或多个节点的状态更新
        for node_name, update in chunk.items():
            print('node_name:', node_name)
            print('update:', update)

            print(f"\n执行节点：{node_name}")

            if not isinstance(update, dict):
                print("状态更新：", update)
                continue

            new_messages = update.get("messages", [])

            for message in new_messages:
                print("消息类型：", type(message).__name__)

                if isinstance(message, AIMessage):
                    if message.tool_calls:
                        print("模型请求工具：", message.tool_calls)
                    elif message.content:
                        print("模型回答：", message.content)

                elif isinstance(message, ToolMessage):
                    print("工具名称：", message.name)
                    print("工具结果：", message.content)

    print("\nAgent 执行结束。")


if __name__ == "__main__":
    main()
