from pydantic import BaseModel, Field
from langchain_core.tools import tool


class OrderQueryInput(BaseModel):
    user_id: str = Field(
        description="当前登录用户的唯一标识"
    )

    order_id: str = Field(
        min_length=1,
        description="需要查询的订单编号，不能为空"
    )


# 模拟订单数据
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


@tool(args_schema=OrderQueryInput)
def get_order(user_id: str, order_id: str) -> dict:
    """根据用户 ID 和订单 ID 查询订单，仅允许查询当前用户自己的订单。"""

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


# 正常调用
result = get_order.invoke({
    "user_id": "USER001",
    "order_id": "ORDER001",
})

print(result)