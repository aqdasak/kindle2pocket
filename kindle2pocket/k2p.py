import requests
import os


class Pocket:
    """
    Pocket Authentication API Documentation
    https://getpocket.com/developer/docs/authentication
    """

    def __init__(self):
        self.consumer_key = os.environ.get('POCKET_API_CONSUMER_KEY')
        self.request_token = None
        self.access_token = None

    def request_access_token(self, redirect_to='#'):
        def get_request_token():
            print('Inside get_request_token()')

            token_request_url = 'https://getpocket.com/v3/oauth/request'
            headers = {'X-Accept': 'application/json'}
            data = {"consumer_key": self.consumer_key,
                    "redirect_uri": "#"
                    }

            response = requests.post(url=token_request_url, headers=headers, data=data)

            # return response.json()['code']

            return response.json()['code']

        def link_to_access_token(request_token, redirect_to='#'):
            print('Inside request_access_token()')

            redirect = 'https://getpocket.com/auth/authorize?request_token=' + request_token + '&redirect_uri=' + redirect_to
            print(redirect)
            return redirect

        link_to_access_token(get_request_token(), redirect_to)

    def get_access_token(self):
        print('Inside get_access_token()')
        headers = {'X-Accept': 'application/json'}
        data = {"consumer_key": self.consumer_key,
                "code": self.request_token}

        authorization_url = 'https://getpocket.com/v3/oauth/authorize'
        response = requests.post(url=authorization_url, headers=headers, data=data)
        # return response.json()['access_token']

        self.access_token = response.json()['access_token']

    def add_item(self, item_url):
        print('Inside add_item()')

        url = 'https://getpocket.com/v3/add'

        headers = {'X-Accept': 'application/json'}
        data = {"url": item_url,
                "tags": "k2p",
                "consumer_key": self.consumer_key,
                "access_token": self.access_token}
        response = requests.post(url=url, headers=headers, data=data)
        print(response.headers)
        print(response.text)

    # rt = get_request_token()
    # print(rt)
    # at = get_access_token(rt)['access_token']
    # print(at)

    # add_item(consumer_key, at, r'https://coderg.herokuapp.com')
