from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)

def normalize(text: str) -> str:
    return text.strip()

def count_chars(text: str) -> int:
    return len(text)

def to_upper(text: str) -> str:
    return text.upper()

def word_count(text: str) -> int:
    return len(text.split())

normalize_runnable = RunnableLambda(normalize)

parallel = RunnableParallel(
    length=RunnableLambda(count_chars),
    uppercase=RunnableLambda(to_upper),
    word_count=RunnableLambda(word_count)
)

# 先规范化，再并行执行两个任务
chain = normalize_runnable | parallel

result = chain.invoke(" Learn LangChain Agent ")

print(result)