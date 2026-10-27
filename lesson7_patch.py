from unittest.mock import patch

def get_model_answer():
    # 假设这是一次真实的大模型调用
    from my_model_client import ask_model
    return ask_model("计算 6 * 7")

def test_get_model_answer():
    with patch(
        "my_model_client.ask_model",
        return_value="42",
    ) as mock_ask:
        # 在 with 代码块内，ask_model 被临时替换
        result = get_model_answer()

        assert result == "42"
        mock_ask.assert_called_once_with("计算 6 * 7")