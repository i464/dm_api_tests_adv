from retrying import retry
from utils.mailhog_tools import (
    get_activation_token_by_login,
    get_confirmation_token_by_email,
)

@retry(stop_max_attempt_number=5, wait_fixed=1000)
def wait_activation_token_by_login(mailhog_api, login: str):
    """
    Wait for registration activation token by login.
    """
    response = mailhog_api.get_api_v2_messages()
    token = get_activation_token_by_login(login, response)
    if not token:
        return None
    return token

@retry(stop_max_attempt_number=5, wait_fixed=1000)
def wait_email_change_token(mailhog_api, new_email: str):
    """
    Wait for email-change confirmation token sent to `new_email`.
    """
    response = mailhog_api.get_api_v2_messages()
    token = get_confirmation_token_by_email(new_email, response)
    if not token:
        return None
    return token
