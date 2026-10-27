from unittest.mock import Mock

from langchain_core.messages import AIMessage, HumanMessage

def test_mock_model_invoke():
    # 模拟大模型的响应
    fake_response = AIMessage(content="42")

    # 创建 Mock 模型对象
    fake_model = Mock()
    fake_model.invoke.return_value = fake_response

    # 像调用真实模型一样调用 invoke
    result = fake_model.invoke(
        [HumanMessage(content="你好")]
    )
    print(result.content)
    # 验证返回值
    assert isinstance(result, AIMessage)
    assert result.content == "42"

    # 验证模型调用行为
    fake_model.invoke.assert_called_once_with(
        [HumanMessage(content="你好")]
    )

if __name__ == "__main__":
    test_mock_model_invoke()
    print("Mock 模型对象测试通过")