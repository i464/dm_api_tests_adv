from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from tests.data.test_data import host_api, host_mailhog, password, login, email
from restclient.configuration import Configuration
from helpers.token_waiters import wait_activation_token_by_login


def test_post_v1_account_login():
    # create configs
    dm_api_config = Configuration(host=host_api)
    mailhog_config = Configuration(host=host_mailhog)

    # create API clients
    account_api = AccountApi(configuration=dm_api_config)
    login_api = LoginApi(configuration=dm_api_config)
    mailhog_api = MailhogApi(configuration=mailhog_config)

    # 1. user registration
    response = account_api.post_v1_account(
        json_data={
            "login": login,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 201, f"User not created: {response.text}"

    # 2. user activation
    activation_token = wait_activation_token_by_login(mailhog_api, login)
    assert activation_token, "Activation token not found"

    response = account_api.put_v1_account_token(token=activation_token)
    assert response.status_code == 200, f"Activation failed: {response.text}"

    # 3. user login
    response = login_api.post_v1_account_login(
        json_data={
            "login": login,
            "password": password,
            "rememberMe": True
        }
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
