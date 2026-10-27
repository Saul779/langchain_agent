
from unittest.mock import Mock


def get_user_name(user_id: int, user_service) -> str:
    """通过外部服务获取用户名。"""
    user = user_service.get_user(user_id)
    return user["name"]


def test_get_user_name():
    # 创建模拟服务
    fake_service = Mock()

    # 规定模拟服务的返回值
    fake_service.get_user.return_value = {
        "id": 456,
        "name": "Bob",
    }
    # 调用被测函数
    result = get_user_name(456, fake_service)
    print(result)
    # 验证业务结果
    assert result == "Bob"

    # 验证外部服务被正确调用
    fake_service.get_user.assert_called_once_with(456)

def test_get_user_name_with_another_user():
    fake_service = Mock()
    fake_service.get_user.return_value = {
        "id": 456,
        "name": "Bob",
    }

    result = get_user_name(456, fake_service)

    assert result == "Bob"
    fake_service.get_user.assert_called_once_with(456)

if __name__ == "__main__":
    test_get_user_name()
    print("Mock 测试通过")
