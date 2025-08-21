from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from restclient.configuration import Configuration
from tests.data.test_data import (
    host_api,
    host_mailhog,
    login,
    password,
    email,
    new_email,
)
from helpers.token_waiters import wait_activation_token_by_login,wait_email_change_token

def test_put_v1_account_email():
    # create API client objects
    dm_api_config = Configuration(host=host_api)
    mailhog_config = Configuration(host=host_mailhog)

    account_api = AccountApi(configuration=dm_api_config)
    login_api = LoginApi(configuration=dm_api_config)
    mailhog_api = MailhogApi(configuration=mailhog_config)

    # register a new user
    response = account_api.post_v1_account(
        json_data={
            "login": login,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 201, f"Registration failed: {response.text}"

    # wait for activation token
    activation_token = wait_activation_token_by_login(mailhog_api, login )
    assert activation_token is not None, "Activation token not found in MailHog"

    response = account_api.put_v1_account_token(token=activation_token)
    assert response.status_code == 200, f"Activation failed: {response.text}"

    # login new user
    response = login_api.post_v1_account_login(
        json_data={
            "login": login,
            "password": password,
            "rememberMe": True
        }
    )
    assert response.status_code == 200, f"Login failed: {response.text}"

    # get X-Dm-Auth-Token from login response headers
    auth_token = response.headers.get("X-Dm-Auth-Token")
    assert auth_token is not None, "No X-Dm-Auth-Token in login response headers"

    # add auth token to AccountApi headers
    account_api.headers = {"X-Dm-Auth-Token": auth_token}

    # send request to change the email
    response = account_api.put_v1_account_email(
        json_data={
            "login": login,
            "password": password,
            "email": new_email
        }
    )
    assert response.status_code == 200, f"Email change request failed: {response.text}"

    # wait for confirmation token sent to new email
    email_change_token = wait_email_change_token(mailhog_api, new_email )
    assert email_change_token, "Email change token not found"

    # confirm new email
    response = account_api.put_v1_account_token(token=email_change_token)
    assert response.status_code == 200, f"Email confirmation failed: {response.text}"

    # verify user can still login
    response = login_api.post_v1_account_login(
        json_data={
            "login": login,
            "password": password,
            "rememberMe": True
        }
    )
    assert response.status_code == 200, f"Login failed: {response.text}"