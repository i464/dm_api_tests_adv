from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    # user registration
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')
    login = 'vm7'
    password = '123456789'
    email = f'{login}@test.de'

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
        'login': 'vm',
        'password': '123456789',
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(
        json_data=json_data
    )
    # print(response.status_code)
    # print(response.text)
    assert response.status_code == 200, "user is not authorized"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']

        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
    return token
