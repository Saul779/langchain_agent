from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from read_env import api_key, model_name, base_url

attempt_count = 0


def query_order_service(order_id: str) -> dict:
    """模拟订单服务：第一次超时，第二次成功。"""
    global attempt_count
    attempt_count += 1

    print(f"订单服务调用次数：{attempt_count}")

    raise TimeoutError("订单服务请求超时")

    # if attempt_count == 1:
    #     raise TimeoutError("订单服务请求超时")
    #
    # return {
    #     "order_id": order_id,
    #     "status": "已支付",
    # }

def query_order_with_retry(
    order_id: str,
    max_attempts: int = 3,
) -> dict:
    """仅对 TimeoutError 重试，最多调用三次。"""

    for attempt in range(1, max_attempts + 1):
        try:
            return query_order_service(order_id)

        except TimeoutError as exc:
            print(f"第 {attempt} 次调用超时：{exc}")

            if attempt == max_attempts:
                raise

    raise RuntimeError("不应执行到这里")

@tool
def get_order_with_retry(order_id: str) -> dict:
    """查询订单状态，遇到临时超时会自动重试。"""
    try:
        return query_order_with_retry(
            order_id,
            max_attempts=3,
        )
    except TimeoutError:
        return {
            "error": "订单服务暂时不可用，请稍后再试",
            "error_type": "timeout",
        }

model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=[get_order_with_retry],
    system_prompt=(
        "你是一个订单服务助手。"
        "查询订单状态时使用 get_order_with_retry。"
        "只能根据工具实际返回的结果回答。"
        "如果工具最终执行失败，应如实告知用户，"
        "如果工具返回 error 字段，必须如实说明失败，"
        "不得把错误结果当作成功结果，也不得编造订单状态和订单信息。"
    ),
)

question = "请查询订单 ORDER001 的状态。"
result = agent.invoke({"messages": [
        {
            "role": "user",
            "content": question,
        }
    ]
})


for message in result["messages"]:
    print(f"\n消息类型：{message.type}")

    if message.type == "human":
        print("用户输入：", message.content)

    elif message.type == "ai":
        print("模型回答：", message.content)

        if message.tool_calls:
            print("工具调用：")
            for call in message.tool_calls:
                print("工具名：", call["name"])
                print("参数：", call["args"])

    elif message.type == "tool":
        print("工具名：", message.name)
        print("工具结果：", message.content)