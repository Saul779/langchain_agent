from langchain_openai import ChatOpenAI
from read_env import api_key, model_name, base_url
from pydantic import BaseModel, Field

model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=0,
)


class CareerInfo(BaseModel):
    occupation: str = Field(
        description="从文本中提取的职业名称"
    )

    skills: list[str] = Field(
        description="文本中明确提及的技能列表"
    )

    years_of_experience: int | None = Field(
        default=None,
        ge=0,
        description="工作年限，必须是非负整数"
    )


structured_model = model.with_structured_output(CareerInfo)

texts = [
    """
    我是一名 Python 测试开发工程师，
    熟悉 Pytest、Playwright 和 LangChain。
    """,
    """
    我是一名 Python 测试开发工程师，
    熟悉 Pytest、Playwright 和 LangChain，
    有 3 年工作经验。
    """,
]

for text in texts:
    try:
        result = structured_model.invoke(
            "从以下文本提取职业信息。只提取明确提供的事实，"
            "未知的工作年限返回 null，不要推测。\n" + text
        )

        print(result.model_dump())
    except Exception as e:
        print(e)