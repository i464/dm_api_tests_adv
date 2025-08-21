from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
from utils.mailhog_tools import get_activation_token_by_login
from tests.data.test_data import host_api, host_mailhog, login, password, email
from restclient.configuration import Configuration
from helpers.token_waiters import wait_activation_token_by_login



def test_put_v1_account_token():
    # create API client objects
    dm_api_config = Configuration(host=host_api)
    mailhog_config = Configuration(host=host_mailhog)

    account_api = AccountApi(configuration=dm_api_config)
    mailhog_api = MailhogApi(configuration=mailhog_config)

    # register user
    response = account_api.post_v1_account(
        json_data={
            "login": login,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 201, f"User not created: {response.text}"

    # wait for activation token
    activation_token = wait_activation_token_by_login(mailhog_api, login )
    assert activation_token is not None, f"Activation token not found in MailHog for {login}"

    # activate user
    response = account_api.put_v1_account_token(token=activation_token)
    assert response.status_code == 200, f"User not activated: {response.text}"
