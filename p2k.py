import requests
import os

'''
Pocket Authentication API Documentation
https://getpocket.com/developer/docs/authentication
'''

consumer_key = os.environ.get('POCKET_API_CONSUMER_KEY')


def get_request_token():
    print('Inside get_request_token()')

    token_request_url = 'https://getpocket.com/v3/oauth/request'
    headers = {'X-Accept': 'application/json'}
    data = {"consumer_key": consumer_key,
            "redirect_uri": "#"
            }

    response = requests.post(url=token_request_url, headers=headers, data=data)

    return response.json()['code']


def get_access_token(request_token):
    print('Inside get_access_token()')

    redirect = 'https://getpocket.com/auth/authorize?request_token=' + request_token + '&redirect_uri=#'
    print(redirect)

    from time import sleep
    sleep(10)

    headers = {'X-Accept': 'application/json'}
    data = {"consumer_key": consumer_key,
            "code": request_token}

    authorization_url = 'https://getpocket.com/v3/oauth/authorize'
    response = requests.post(url=authorization_url, headers=headers, data=data)
    return response.json()


def add_item(consumer_key, access_token, item_url):
    print('Inside add_item()')

    url = 'https://getpocket.com/v3/add'

    headers = {'X-Accept': 'application/json'}
    data = {"url": item_url,
            "tags": "p2k",
            "consumer_key": consumer_key,
            "access_token": access_token}
    response = requests.post(url=url, headers=headers, data=data)
    print(response.headers)
    print(response.text)


rt = get_request_token()
print(rt)
at = get_access_token(rt)['access_token']
print(at)
add_item(consumer_key, at, r'http://coderg.herokuapp.com')
