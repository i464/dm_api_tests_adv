
from utils.mailhog_tools import get_activation_token_by_login

class AccountHelper:
    def __init__(self, dm_account_api, mailhog):
        """
        dm_account_api: fasade with .account_api и .login_api
        mailhog: fasade with .mailhog_api
        """
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def user_login(self, login: str, password: str, remember_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f"User not authorized: {response.text}"
        return response

    def register_new_user(self, login: str, email: str, password: str):
        # 1) register
        response = self.dm_account_api.account_api.post_v1_account(json_data={
            'login': login,
            'email': email,
            'password': password
        })
        assert response.status_code == 201, f"User not created: {response.text}"

        # 2) read mail
        response_mail = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response_mail.status_code == 200, f"No emails: {response_mail.text}"

        # 3) extract token
        token = get_activation_token_by_login(login, response_mail)
        assert token, f"No activation token for {login}"

        # 4) activate
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"User not activated: {response.text}"
        return response
