import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 加载 .env 文件，只需要在程序入口执行一次
# 会自动读取项目根目录下的 .env
load_dotenv()

# 读取配置
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

base_url = LLM_BASE_URL
api_key = LLM_API_KEY
model_name = LLM_MODEL_NAME

# 校验：防止忘记配置
if not all([LLM_BASE_URL, LLM_API_KEY, LLM_MODEL_NAME]):
    raise ValueError("请检查 .env 文件，LLM_BASE_URL、LLM_API_KEY、LLM_MODEL_NAME 不能为空")


# 【方式1：普通函数直接使用】
def test_llm_config():
    print(f"base_url: {LLM_BASE_URL}")
    print(f"api_key: {LLM_API_KEY}")
    print(f"model: {LLM_MODEL_NAME}")


# 【方式2：LangChain 创建 LLM 对象】
def get_llm():
    llm = ChatOpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
        model=LLM_MODEL_NAME,
        temperature=0.7
    )
    return llm


if __name__ == "__main__":
    test_llm_config()
    # llm = get_llm()
    # resp = llm.invoke("你好")
    # print(resp.content)
