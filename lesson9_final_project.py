
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI

from read_env import api_key, model_name, base_url


model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    temperature=0,
    base_url=base_url,
)


# 1. 规范化文本，不修改原始字典
def normalize_input(data: dict) -> dict:
    return {
        **data,
        "text": data["text"].strip(),
    }


# 2. 统计字符数
def count_chars(data: dict) -> int:
    return len(data["text"])


# 3. 统计单词数
def count_words(data: dict) -> int:
    return len(data["text"].split())


# 4. 转换成大写字符串
def text_upper(data: dict) -> str:
    return data["text"].upper()


# 5. 构建摘要链
prompt = ChatPromptTemplate.from_template(
    "请用不超过100字概括下面的文本，"
    "只输出摘要，不要添加其他说明。\n\n"
    "文本：\n{text}"
)

summary_chain = prompt | model | StrOutputParser()


# 6. 摘要异常处理：将异常转为明确的结果
def safe_summary(data: dict) -> str:
    try:
        return summary_chain.invoke(data)
    except Exception as exc:
        # 教学示例：实际项目应记录日志并区分异常类型
        return f"摘要生成失败：{type(exc).__name__}"


# 7. 组合完整 LCEL 链
analysis_chain = (
    RunnableLambda(normalize_input) | RunnablePassthrough.assign(
        char_count=RunnableLambda(count_chars),
        word_count=RunnableLambda(count_words),
        uppercase=RunnableLambda(text_upper),
        summary=RunnableLambda(safe_summary),
    )
)


# 8. 一次调用执行完整流程
result = analysis_chain.invoke({
    "text": "  LangChain helps developers build LLM applications.  "
})


print("原始文本：", result["text"])
print("字符数：", result["char_count"])
print("单词数：", result["word_count"])
print("大写文本：", result["uppercase"])
print("摘要：", result["summary"])
print("结果类型：", type(result))
print("摘要类型：", type(result["summary"]))