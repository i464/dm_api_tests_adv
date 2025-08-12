from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from tests.helpers.mailhog_tools import get_activation_token_by_login
from tests.helpers.test_data import host_api, host_mailhog, login, password, email


def test_post_v1_account_login():
    account_api = AccountApi(host=host_api)
    login_api = LoginApi(host=host_api)
    mailhog_api = MailhogApi(host=host_mailhog)

    # Register user
    response = account_api.post_v1_account(
        json_data={
            "login": login,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 201, f"User not created: {response.text}"

    # Get token
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "No emails received"

    token = get_activation_token_by_login(login, response)
    assert token is not None, "Activation token not found"

    # Activate user
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "User not activated"

    # Login
    response = login_api.post_v1_account_login(
        json_data={
            "login": login,
            "password": password,
            "rememberMe": True
        }
    )
    assert response.status_code == 200, "User failed to login"
