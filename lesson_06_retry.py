
import time


def retry_call(operation, max_attempts=3, delay=1):
    """仅重试 TimeoutError，达到最大次数后抛出异常。"""
    if max_attempts < 1:
        raise ValueError("max_attempts 必须大于等于 1")

    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"开始第 {attempt} 次调用")
            return operation()

        except TimeoutError as exc:
            last_error = exc
            print(f"第 {attempt} 次调用超时：{exc}")

            if attempt < max_attempts:
                wait_seconds = delay * (2 ** (attempt - 1))
                print(f"等待 {wait_seconds} 秒后重试")
                time.sleep(wait_seconds)

    raise RuntimeError(
        f"连续失败，已尝试 {max_attempts} 次"
    ) from last_error


# 模拟前两次超时，第三次成功
attempt_count = 0


def unstable_operation():
    global attempt_count
    attempt_count += 1

    if attempt_count < 3:
        raise TimeoutError("模拟网络超时")

    return "接口调用成功"


result = retry_call(
    unstable_operation,
    max_attempts=3,
    delay=1,
)

print("最终结果：", result)



from langchain_core.tools import tool


attempt_count = 0


def simulated_api():
    global attempt_count
    attempt_count += 1

    if attempt_count < 3:
        raise TimeoutError("模拟外部 API 超时")

    return {"status": "ok", "attempt": attempt_count}


@tool
def query_remote_service() -> str:
    """查询一个模拟的外部服务。"""
    result = retry_call(
        simulated_api,
        max_attempts=3,
        delay=0,
    )
    return str(result)


print(query_remote_service.invoke({}))
