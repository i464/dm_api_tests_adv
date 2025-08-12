from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from tests.helpers.mailhog_tools import get_activation_token_by_login
from tests.helpers.test_data import (
    host_api,
    host_mailhog,
    login,
    password,
    email
)

def test_post_v1_account():
    # user registration
    account_api = AccountApi(host=host_api)
    login_api = LoginApi(host=host_api)
    mailhog_api = MailhogApi(host=host_mailhog)

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.post_v1_account(
        json_data=json_data
    )
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"User not created{response.json()}"

    # get emails from server
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "no emails "
    #   pprint.pprint(response.json())

    # get token
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"No Token for {login} user"

    # user verification
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "user is not activated"

    # authorisation
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(
        json_data=json_data
    )

    # print(response.status_code)
    # print(response.text)
    assert response.status_code == 200, "user is not authorized"


