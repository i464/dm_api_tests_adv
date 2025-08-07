import pprint
from os.path import split

import requests
from json import loads


def test_post_v1_account():
    # user registration
    login = 'vm3'
    password = '123456789'
    email = f'{login}@test.de'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201 , f"User not created{response.json()}"

    # get emails from server
    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "no emails "
    #   pprint.pprint(response.json())

    # get token
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']

        if user_login == login:

            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)

    assert token is not None,f"No Token for {login} user"

    # user verification

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "user is not activated"

    # authorisation


json_data = {
    'login': 'vm',
    'password': '123456789',
    'rememberMe': True,
}

response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
# print(response.status_code)
# print(response.text)
assert response.status_code == 200, "user is not authorized"