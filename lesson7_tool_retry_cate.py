def query_order_service(
    order_id: str,
    error_type: str = "timeout",
) -> dict:
    """模拟不同类型的订单服务故障。"""

    print(f"执行订单查询：{order_id}")

    if error_type == "timeout":
        raise TimeoutError("订单服务请求超时")

    if error_type == "invalid":
        raise ValueError("订单号格式不合法")

    return {
        "order_id": order_id,
        "status": "已支付",
    }

def query_order_with_retry(
    order_id: str,
    error_type: str = "timeout",
    max_attempts: int = 3,
) -> dict:
    for attempt in range(1, max_attempts + 1):
        try:
            return query_order_service(
                order_id,
                error_type,
            )

        except TimeoutError as exc:
            print(f"第 {attempt} 次调用超时：{exc}")

            if attempt == max_attempts:
                return {
                    "error": "订单服务暂时不可用",
                    "error_type": "timeout",
                }

        except ValueError as exc:
            print(f"参数或数据错误，不重试：{exc}")
            return {
                "error": str(exc),
                "error_type": "invalid_input",
            }

# 测试 A：超时，验证最多尝试三次
print("=== 测试 A：超时 ===")
print(query_order_with_retry("ORDER001", "timeout"))

# 测试 B：参数错误，验证立即失败
print("\n=== 测试 B：参数错误 ===")
print(query_order_with_retry("INVALID", "invalid"))

# 测试 C：正常查询
print("\n=== 测试 C：正常查询 ===")
print(query_order_with_retry("ORDER001", "success"))