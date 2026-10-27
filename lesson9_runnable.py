from langchain_core.runnables import RunnableLambda


def normalize_text(text: str) -> str:
    """去除首尾空格，并转换为大写。"""
    return text.strip().upper()


def count_chars(text: str) -> int:
    """统计字符数量。"""
    return len(text)

def add_prefix(text: str)-> str:
    """为文本添加前缀"""

    return "结果为: {}".format(text)

# 将普通 Python 函数包装成 Runnable
normalize_runnable = RunnableLambda(normalize_text)
count_runnable = RunnableLambda(count_chars)
add_prefix = RunnableLambda(add_prefix)

# 使用 LCEL 将两个 Runnable 组合起来
chain = normalize_runnable | count_runnable | add_prefix

# 执行整个处理链
result = chain.invoke("hello")

print(result)