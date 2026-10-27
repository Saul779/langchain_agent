
from langchain_core.tools import tool, ToolException

attempt_count = 0


@tool
def unstable_query() -> str:
    """查询模拟的外部服务，前两次调用会超时。"""
    global attempt_count
    attempt_count += 1

    print(f"实际调用次数：{attempt_count}")

    if attempt_count < 3:
        raise TimeoutError("模拟网络超时")

    return "查询成功"


# 对工具添加重试策略
retryable_tool = unstable_query.with_retry(
    retry_if_exception_type=(TimeoutError,),
    stop_after_attempt=3,
    wait_exponential_jitter=True,
)

result = retryable_tool.invoke({})

print("最终结果：", result)
