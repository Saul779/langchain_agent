
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)
from read_env import (LLM_BASE_URL,LLM_API_KEY,LLM_MODEL_NAME)

def main():
    base_url = LLM_BASE_URL
    api_key = LLM_API_KEY
    model_name = LLM_MODEL_NAME

    if not api_key:
        raise RuntimeError("请先设置 OPENAI_API_KEY")

    if not model_name:
        raise RuntimeError("请先设置 OPENAI_MODEL")

    model_kwargs = {
        "model": model_name,
        "api_key": api_key,
        "temperature": 0.5,
    }

    if base_url:
        model_kwargs["base_url"] = base_url

    model = ChatOpenAI(**model_kwargs)

    messages = [
        SystemMessage(
            content="你是一名 Python 和 AI Agent 教师，回答简洁准确。"
        ),
        HumanMessage(
            content="请用不超过100字解释什么是 ReAct Agent。"
        ),
    ]

    response = model.invoke(messages)

    print("返回对象类型：", type(response).__name__)
    print("回答内容：", response.content)
    print("模型元数据：", response.response_metadata)


if __name__ == "__main__":
    main()
