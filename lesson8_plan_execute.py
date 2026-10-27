from typing import TypedDict
from langgraph.graph import END, START, StateGraph


class PlanExecuteState(TypedDict):
    task: str
    plan: list[str]
    current_step: int
    results: list[str]


def planner(state: PlanExecuteState) -> dict:
    """根据任务生成固定的演示计划。"""
    print("\n[Planner] 正在生成计划")

    plan = [
        "读取测试报告",
        "统计失败用例",
        "生成总结",
    ]

    print(f"[Planner] 计划：{plan}")

    return {
        "plan": plan,
        "current_step": 0,
        "results": [],
    }


def executor(state: PlanExecuteState) -> dict:
    """执行当前步骤，并将结果写回状态。"""
    index = state["current_step"]
    step = state["plan"][index]

    print(f"\n[Executor] 执行步骤 {index + 1}：{step}")

    # 暂时用模拟结果代替真实工具或大模型
    result = f"步骤完成：{step}"

    return {
        "results": state["results"] + [result],
        "current_step": index + 1,
    }


def route_after_execute(state: PlanExecuteState) -> str:
    """判断是否还有未执行的步骤。"""
    if state["current_step"] < len(state["plan"]):
        return "execute"

    return "finish"


builder = StateGraph(PlanExecuteState)

builder.add_node("planner", planner)
builder.add_node("executor", executor)

builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")

builder.add_conditional_edges(
    "executor",
    route_after_execute,
    {
        "execute": "executor",
        "finish": END,
    },
)

app = builder.compile()


if __name__ == "__main__":
    initial_state: PlanExecuteState = {
        "task": "分析一份软件测试报告",
        "plan": [],
        "current_step": 0,
        "results": [],
    }

    final_state = app.invoke(initial_state)

    print("\n最终结果：")
    print(final_state)