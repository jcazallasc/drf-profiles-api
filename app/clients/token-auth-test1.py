import requests


def client():
    token_h = 'Token 44600f1a60de3b30bc51c55a57695bd98cef05ee'

    # credentials = {'username': 'jcazallasc@gmail.com', 'password': 'cazallas'}

    # response = requests.post(
    #     'http://127.0.0.1:8000/api/rest-auth/login/',
    #     data=credentials,
    # )

    response = requests.get(
        'http://127.0.0.1:8000/api/profiles/',
        headers={'Authorization': token_h},
    )

    print('status_code', response.status_code)
    print(response.json())


if __name__ == "__main__":
    client()
