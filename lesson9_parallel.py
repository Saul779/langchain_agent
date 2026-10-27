from langchain_core.runnables import RunnableLambda, RunnableParallel

# 定义两个普通 Python 函数
def count_chars(text: str) -> int:
    return len(text)

def to_upper(text: str) -> str:
    return text.upper()

# 将两个函数包装成 Runnable，并行组合
parallel = RunnableParallel(
    length=RunnableLambda(count_chars),
    uppercase=RunnableLambda(to_upper),
)

result = parallel.invoke("LangChain Agent")

print(result)
print(type(result))