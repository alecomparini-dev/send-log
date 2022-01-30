import requests


class OAuthService:
    def __init__(self, url, user, password):
        self._token = None
        self._url = url
        self._user = user
        self._password = password

    def _get_new_token(self):
        body = {
            'user': self._user,
            'password': self._password
        }

        resp = requests.post(url=self._url, json=body, headers={'Content-Type': 'application/json'})
        token_resp = resp.json()

        return token_resp['access_token']

    @property
    def token(self):
        if not self._token:
            self._token = self._get_new_token()
        return self._token

    def clean(self):
        self._token = None
