import requests


def test_post_v1_account():
    # user registration
    login = 'vm_test'
    password= '123456789'
    email = f'{login}@test.de'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # get emails from server
    params = {
        'limit': '50'
    }
    response = requests.get(
        'http://5.63.153.31:5025/api/v1/messages/Hj7z0T5RDfx1WVVnY1btlLahbWwJ20fmKRoo0YnwWBQ=@mailhog.example',
        params=params,verify=False
    )
    print(response.status_code)
    print(response.text)

    # get token
    ...
    # user verification

    response = requests.put('http://5.63.153.31:5051/v1/account/fc5c9258-0e89-4d18-8f5d-aabbb4d5e05e')
    print(response.status_code)
    print(response.text)

    # authorisation

    json_data = {
        'login': login,
        'email': email,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/password', json=json_data)
    print(response.status_code)
    print(response.text)
