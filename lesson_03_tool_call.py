
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
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
    model_with_tools = model.bind_tools([multiply])

    question = "请使用乘法工具计算 237 乘以 419。"
    messages = [HumanMessage(content=question)]

    # 第一次模型调用：获取回答或工具调用请求
    response = model_with_tools.invoke(messages)

    print("第一次返回对象：", type(response).__name__)
    print("模型文本：", response.content)
    print("工具调用请求：", response.tool_calls)

    # 保存模型返回的消息，供后续模型调用使用
    messages.append(response)
    print("第一次请求的response:{}".format(response))
    print("第一次请求的response数据类型:{}".format(type(response)))

    # 手动执行模型请求的工具
    for tool_call in response.tool_calls:
        if tool_call["name"] != "multiply":
            raise ValueError(
                f"不支持的工具：{tool_call['name']}"
            )

        result = multiply.invoke(tool_call["args"])

        print("工具执行结果：", result)

        # 将执行结果反馈给模型
        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )

    # 如果模型请求了工具，再调用模型生成最终回答
    if response.tool_calls:
        final_response = model_with_tools.invoke(messages)
        print("最终回答：", final_response.content)
    else:
        print("模型没有请求工具，请检查模型服务的工具调用支持。")


if __name__ == "__main__":
    main()
