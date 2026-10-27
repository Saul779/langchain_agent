from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI

from read_env import api_key, model_name, base_url


# 1. 初始化模型：沿用当前项目的配置
model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    temperature=0,
    base_url=base_url,
)


# 2. 定义 Python 计算函数
def count_chars(data: dict) -> int:
    return len(data["text"])


def count_words(data: dict) -> int:
    return len(data["text"].split())


# 3. 定义摘要提示词
prompt = ChatPromptTemplate.from_template(
    "请用不超过100字概括下面的文本，"
    "只输出摘要，不要添加其他说明。\n\n"
    "文本：\n{text}"
)


# 4. 组合大模型摘要链
summary_chain = prompt | model | StrOutputParser()


# 5. 组合完整分析链
analysis_chain = RunnablePassthrough.assign(
    char_count=RunnableLambda(count_chars),
    word_count=RunnableLambda(count_words),
    summary=summary_chain,
)


# 6. 执行
result = analysis_chain.invoke({
    "text":
        "LangChain 是一个用于开发大语言模型应用的框架。它提供提示词模板、模型接口、输出解析器和工具调用等能力。开发者可以使用 LCEL 将不同组件组合成可复用的处理链。"

})


# 7. 检查输出
print("原始文本：", result["text"])
print("字符数：", result["char_count"])
print("单词数：", result["word_count"])
print("摘要：", result["summary"])
print("结果类型：", type(result))