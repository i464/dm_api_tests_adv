import requests
from restclient.client import RestClient


class AccountApi(RestClient):

    def set_headers(self,
                    headers):
        self.headers = headers

    def post_v1_account(self,
                        json_data):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(self,
                             token):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path = f'/v1/account/{token}',
            headers = headers
        )
        return response

    def put_v1_account_email(self,
                             json_data):
        """
        Change user email
        :param json_data: {"email": "new_email@example.com"}
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/email',
            headers=self.headers,
            json=json_data
        )
        return response

