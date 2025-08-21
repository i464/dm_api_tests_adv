from helpers.token_waiters import wait_activation_token_by_login, wait_email_change_token

class AccountHelper:
    def __init__(self, dm_account_api, mailhog):
        """
        dm_account_api: facade with .account_api и .login_api
        mailhog: facade with .mailhog_api
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
        """
        1) Register user
        2) Wait for activation token via MailHog (smart waiter with retries)
        3) Activate user
        """
        # Step 1 register
        response = self.dm_account_api.account_api.post_v1_account(json_data={
            'login': login,
            'email': email,
            'password': password
        })
        assert response.status_code == 201, f"User not created: {response.text}"

        # Step 2 wait for activation token (no manual parsing here)
        token = wait_activation_token_by_login(self.mailhog.mailhog_api, login)
        assert token, f"No activation token for {login}"

        # Step 3 activate
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"User not activated: {response.text}"
        return response