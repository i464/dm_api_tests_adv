from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from tests.helpers.mailhog_tools import get_activation_token_by_login
from tests.helpers.test_data import host_api, host_mailhog, login, password, email


def test_post_v1_account():
    account_api = AccountApi(host=host_api)
    login_api = LoginApi(host=host_api)
    mailhog_api = MailhogApi(host=host_mailhog)

    # 1. Register new user
    response = account_api.post_v1_account(
        json_data={
            'login': login,
            'email': email,
            'password': password
        }
    )
    assert response.status_code == 201, f"User not created: {response.text}"

    # 2. Get emails from Mailhog
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "No emails received"

    # 3. Get activation token
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"No token for {login}"

    # 4. Activate user
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "User not activated"

    # 5. Login
    response = login_api.post_v1_account_login(
        json_data={
            'login': login,
            'password': password,
            'rememberMe': True
        }
    )
    assert response.status_code == 200, "User not authorized"
