from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
from tests.helpers.mailhog_tools import get_activation_token_by_login
from tests.helpers.test_data import host_api, host_mailhog, login, password, email


def test_put_v1_account_token():
    account_api = AccountApi(host=host_api)
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

    # Get token from Mailhog
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, f"No emails received: {response.text}"

    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Activation token not found for {login}"

    # Activate user
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"User not activated: {response.text}"
