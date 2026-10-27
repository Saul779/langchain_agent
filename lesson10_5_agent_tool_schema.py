from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from read_env import api_key, model_name, base_url


# 1. 定义工具参数 schema
class OrderQueryInput(BaseModel):
    user_id: str = Field(
        description="查询订单所属的用户 ID"
    )
    order_id: str = Field(
        min_length=1,
        description="需要查询的订单编号"
    )


# 2. 模拟订单数据
ORDERS = {
    "ORDER001": {
        "user_id": "USER001",
        "amount": 199.0,
        "status": "已支付",
    },
    "ORDER002": {
        "user_id": "USER002",
        "amount": 399.0,
        "status": "待支付",
    },
}


# 3. 定义查询工具
@tool(args_schema=OrderQueryInput)
def get_order(user_id: str, order_id: str) -> dict:
    """查询指定用户自己的订单信息。"""

    order = ORDERS.get(order_id)

    if order is None:
        return {"error": "订单不存在"}

    if order["user_id"] != user_id:
        return {"error": "无权访问该订单"}

    return {
        "order_id": order_id,
        "amount": order["amount"],
        "status": order["status"],
    }


@tool
def get_logistics(order_id: str) -> dict:
    """查询指定订单的物流信息。需要提供订单号。"""
    logistics_data = {
        "ORDER001": {
            "status": "运输中",
            "location": "重庆转运中心",
        }
    }

    return logistics_data.get(
        order_id, {"error": "未找到物流信息"},
    )


@tool
def get_refund_status(order_id: str) -> dict:
    """查询指定订单的退款进度。需要提供订单号。"""
    refund_data = {
        "ORDER002": {
            "status": "退款处理中",
        }
    }

    return refund_data.get(
        order_id,
        {"error": "未找到退款记录"},
    )


# 4. 初始化模型
model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=0,
)


# 5. 创建 Agent
agent = create_agent(
    model=model,
    tools=[get_order,
        get_logistics,
        get_refund_status,
           ],
    system_prompt=(
        "你是一个订单服务助手。"
        "根据用户请求选择必要的工具。"
        "查询订单金额或状态时使用 get_order。"
        "查询物流时使用 get_logistics。"
        "查询退款时使用 get_refund_status。"
        "当用户同时询问订单状态和物流信息时，"
        "必须分别获取订单信息和物流信息。"
        "只能根据工具实际返回的结果回答，"
        "不得编造订单或物流信息。"
        "不要调用与用户请求无关的工具。"
    ),
)


# 6. 调用 Agent
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "请查询 USER001 的订单 ORDER001 的状态，并告诉我物流到哪里了。",
        }
    ]
})


# 7. 查看最终回答
# for message in result["messages"]:
#     # if message.type == "ai":
#     #     print("工具调用：", getattr(message, "tool_calls", []))
#     #
#     # if message.type == "tool":
#     #     print("工具名称：", getattr(message, "name", None))
#
#     if message.type == "ai" and not message.content:
#         print(f"{message.type}: {message.tool_calls}")
#         continue
#     print(f"{message.type}: {message.content}")


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



# questions = [
#     "请查询 USER001 的订单 ORDER001，告诉我金额和状态。",
#     "请查询订单 ORDER001 的物流信息。",
#     "请查询订单 ORDER002 的退款进度。",
# ]

# for question in questions:
#     result = agent.invoke({
#         "messages": [
#             {"role": "user", "content": question}
#         ]
#     })
#
#     for message in result["messages"]:
#         print(message.type, message.content)
#         if getattr(message, "tool_calls", None):
#             print("工具调用：", message.tool_calls)