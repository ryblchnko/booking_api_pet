import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "user_id, email, is_present",
    [
        (1, "fedor@moloko.ru", True),
        (2, "sharik@moloko.ru", True),
        (4, "test@user.com", False),
    ],
)
async def test_find_user_bt_id(user_id, email, is_present):
    user = await UserDAO.find_by_id(user_id)

    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
