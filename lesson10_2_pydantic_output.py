from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from read_env import api_key, model_name, base_url


class CareerInfo(BaseModel):
    occupation: str = Field(
        description="从文本中提取的职业名称"
    )

    skills: list[str] = Field(
        description="文本中明确提及的技能列表"
    )

    years_of_experience: int = Field(
        ge=0,
        description="工作年限，必须是非负整数"
    )


model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=0,
)

structured_model = model.with_structured_output(CareerInfo)

text = """
我是一名 Python 测试开发工程师，熟悉
Pytest、Playwright 和 LangChain，有 3 年工作经验。
"""

result = structured_model.invoke(
    f"请从以下文本提取职业、技能和工作年限：\n{text}"
)

print(result)
print(type(result))

print(result.occupation)
print(result.skills)
print(result.years_of_experience)

print(result.model_dump())