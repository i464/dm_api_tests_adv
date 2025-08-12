from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from tests.helpers.test_data import (
    host_api, host_mailhog, login, password, email, new_email
)
from tests.helpers.mailhog_tools import (
    get_activation_token_by_login,
    get_confirmation_token_by_email,
)


def test_change_email_e2e():
    account_api = AccountApi(host=host_api)
    login_api = LoginApi(host=host_api)
    mailhog_api = MailhogApi(host=host_mailhog)

    # 1 Register new user
    print("STEP 1: Register new user")
    response = account_api.post_v1_account(
        json_data={"login": login, "email": email, "password": password}
    )
    assert response.status_code == 201, f"Registration failed: {response.text}"

    # 2 Get activation token from mail (by login)
    print("STEP 2: Get activation token from Mailhog by login")
    messages_response = mailhog_api.get_api_v2_messages()
    activation_token = get_activation_token_by_login(login, messages_response)
    assert activation_token is not None, "Activation token not found in Mailhog"

    # 3 Activate user
    print("STEP 3: Activate user with token")
    response = account_api.put_v1_account_token(token=activation_token)
    assert response.status_code == 200, f"Activation failed: {response.text}"

    # 4 Log in
    print("STEP 4: Log in")
    response = login_api.post_v1_account_login(
        json_data={"login": login, "password": password, "rememberMe": True}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"

    # 5 Change email
    print("STEP 5: Change email (authorized request)")
    auth_token = response.headers.get("X-Dm-Auth-Token")
    assert auth_token is not None, "No X-Dm-Auth-Token in login response headers"

    if hasattr(account_api, "set_headers"):
        account_api.set_headers({"X-Dm-Auth-Token": auth_token})
    else:
        account_api.headers = {"X-Dm-Auth-Token": auth_token}

    response = account_api.put_v1_account_email(
        json_data={"login": login, "password": password, "email": new_email}
    )
    assert response.status_code == 200, f"Email change request failed: {response.text}"

    # 6) Try login again — expect 403 (new email not confirmed yet)
    print("STEP 6: Try login again (expect 403)")
    response = login_api.post_v1_account_login(
        json_data={"login": login, "password": password, "rememberMe": True}
    )
    assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.text}"

    # 7) Get confirmation token for the NEW email (search by To header == new_email)
    print("STEP 7: Get confirmation token for NEW email from Mailhog")
    messages_response = mailhog_api.get_api_v2_messages()
    new_email_token = get_confirmation_token_by_email(new_email, messages_response)
    assert new_email_token is not None, "No confirmation token for the new email"

    # 8) Confirm new email
    print("STEP 8: Confirm new email with token")
    response = account_api.put_v1_account_token(token=new_email_token)
    assert response.status_code == 200, f"New email activation failed: {response.text}"

    # 9) Login again — now should succeed (200)
    print("STEP 9: Final login ")
    response = login_api.post_v1_account_login(
        json_data={"login": login, "password": password, "rememberMe": True}
    )
    assert response.status_code == 200, f"Login after new email confirmation failed: {response.text}"
