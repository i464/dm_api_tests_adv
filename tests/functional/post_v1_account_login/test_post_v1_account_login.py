from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from utils.mailhog_tools import get_activation_token_by_login
from tests.data.test_data import host_api, host_mailhog, password, login, email


def test_post_v1_account_login():
    account_api = AccountApi(host=host_api)
    login_api = LoginApi(host=host_api)
    mailhog_api = MailhogApi(host=host_mailhog)

    # 1. Регистрация пользователя
    response = account_api.post_v1_account(
        json_data={
            "login": login,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 201, f"User not created: {response.text}"

    # 2. Активация пользователя
    messages = mailhog_api.get_api_v2_messages()
    activation_token = get_activation_token_by_login(login, messages)
    assert activation_token, "Activation token not found"

    response = account_api.put_v1_account_token(token=activation_token)
    assert response.status_code == 200, f"Activation failed: {response.text}"

    # 3. Логин пользователя
    response = login_api.post_v1_account_login(
        json_data={
            "login": login,
            "password": password,
            "rememberMe": True
        }
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
