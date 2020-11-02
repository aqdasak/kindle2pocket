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

            # self.request_token=response.json()['code']
            # print(self.request_token)
            print(response.text)

        def link_to_access_token(redirect_to='#'):
            print('Inside link_to_access_token()')

            redirect = 'https://getpocket.com/auth/authorize?request_token=' + self.request_token + '&redirect_uri=' + redirect_to
            print(redirect)
            return redirect

        get_request_token()
        return link_to_access_token(redirect_to)

    def get_access_token(self):
        print('Inside get_access_token()')
        headers = {'X-Accept': 'application/json'}
        data = {"consumer_key": self.consumer_key,
                "code": self.request_token}

        authorization_url = 'https://getpocket.com/v3/oauth/authorize'
        response = requests.post(url=authorization_url, headers=headers, data=data)

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


if __name__ == '__main__':
    ob = Pocket()
    rt = ob.request_access_token()
    # print('Click =',rt)
    import time
    time.sleep(10)
    ob.get_access_token()
    ob.add_item(r'https://www.google.com')
