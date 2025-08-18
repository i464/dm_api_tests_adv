from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from utils.mailhog_tools import get_activation_token_by_login, get_confirmation_token_by_email
from tests.data.test_data import host_api, host_mailhog, login, password, email, new_email


def test_put_v1_account_email():
    # STEP 1: Create API client objects
    account_api = AccountApi(host=host_api)
    login_api = LoginApi(host=host_api)
    mailhog_api = MailhogApi(host=host_mailhog)

    # STEP 2: Register a new user
    response = account_api.post_v1_account(
        json_data={
            "login": login,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 201, f"Registration failed: {response.text}"

    # STEP 3: Get activation token from MailHog
    messages_response = mailhog_api.get_api_v2_messages()
    activation_token = get_activation_token_by_login(login, messages_response)
    assert activation_token is not None, "Activation token not found in MailHog"

    # STEP 4: Activate the user
    response = account_api.put_v1_account_token(token=activation_token)
    assert response.status_code == 200, f"Activation failed: {response.text}"

    # STEP 5: Log in with the new user
    response = login_api.post_v1_account_login(
        json_data={
            "login": login,
            "password": password,
            "rememberMe": True
        }
    )
    assert response.status_code == 200, f"Login failed: {response.text}"

    # STEP 6: Get X-Dm-Auth-Token from login response headers
    auth_token = response.headers.get("X-Dm-Auth-Token")
    assert auth_token is not None, "No X-Dm-Auth-Token in login response headers"

    # STEP 7: Add auth token to AccountApi headers
    account_api.headers = {"X-Dm-Auth-Token": auth_token}

    # STEP 8: Send request to change the email
    response = account_api.put_v1_account_email(
        json_data={
            "login": login,
            "password": password,
            "email": new_email
        }
    )
    assert response.status_code == 200, f"Email change request failed: {response.text}"

    # STEP 9: Get confirmation token for the new email from MailHog
    messages_response = mailhog_api.get_api_v2_messages()
    email_change_token = get_confirmation_token_by_email(new_email, messages_response)
    assert email_change_token is not None, "Email change token not found"

    # STEP 10: Confirm the new email
    response = account_api.put_v1_account_token(token=email_change_token)
    assert response.status_code == 200, f"Email confirmation failed: {response.text}"
