import random
from langchain_core.tools import tool,ToolException

attempt_count = 3

@tool
def request_sample_1(a):
    global attempt_count
    rand_int = random.randint(1,3)
    if rand_int == 1:
        attempt_count -= 1
        raise TimeoutError('请求超时')
    return 1

try:
    request_sample_1.invoke(1)
except TimeoutError as e:
    request_sample_1.invoke(1)