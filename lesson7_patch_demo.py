from unittest.mock import patch


def get_model_answer():
    return ask_model("计算 6 * 7")


def ask_model(prompt: str) -> str:
    # 模拟真实项目中的外部模型调用
    raise RuntimeError("这里不应该调用真实模型")


def test_get_model_answer():
    with patch(__name__ + ".ask_model",return_value="42",
    ) as mock_ask:
        result = get_model_answer()

        assert result == "42"
        mock_ask.assert_called_once_with("计算 6 * 7")


if __name__ == "__main__":
    test_get_model_answer()
    print("patch 测试通过")
