from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from read_env import (
    api_key,
    model_name,
    base_url)

model_kwargs = {
    "model": model_name,
    "api_key": api_key,
    "temperature": 0,
    "base_url": base_url
}
model = ChatOpenAI(**model_kwargs)

prompt = ChatPromptTemplate.from_template(
    "请用简单的语言解释什么是{topic}，并举一个例子。"
)

parser = StrOutputParser()

# 使用 LCEL 组合三个步骤
chain = prompt | model | parser

# 执行整个链
result = chain.invoke({"topic": "Runnable"})

print(result)
print(type(result))
print(isinstance(result, str))