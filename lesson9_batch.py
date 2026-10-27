from langchain_core.runnables import RunnableLambda


def normalize_text(text: str) -> str:
    return text.strip().upper()


chain = RunnableLambda(normalize_text)

texts = [" hello ", " python ", " LangChain ", " agent "]

results = chain.batch(texts)

print(results)