import requests


def client():
    id = 12
    data = {
        'username': 'test{}'.format(id),
        'email': 'test{}@test.com'.format(id),
        'password1': 'changeme123',
        'password2': 'changeme123',
    }

    response = requests.post(
        'http://127.0.0.1:8000/api/rest-auth/registration/',
        data=data,
    )

    print('status_code', response.status_code)
    print(response.json())


if __name__ == "__main__":
    client()
