from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)


def count_chars(data: dict) -> int:
    return len(data["text"])

def to_upper(data: dict) -> str:
    return data["text"].upper()

def word_count(data: dict) -> int:
    return len(data['text'].split())

def text_strip(data: dict) -> int:
    return data['text'].strip()

def text_length_with_spaces(data: dict) -> int:
    return len(data["text"])

chain = RunnablePassthrough.assign(
    char_count=RunnableLambda(count_chars),
    uppercase=RunnableLambda(to_upper),
    word_count=RunnableLambda(word_count),
    text_strip=RunnableLambda(text_strip),
    text_length_with_spaces=RunnableLambda(text_length_with_spaces),
)

result = chain.invoke({
    "text": " LangChain Agent "
})

print(result)