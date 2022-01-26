import requests
from dotenv import dotenv_values
config = dotenv_values(".env")

class OAuth:

    _client_id = config['CLIENT_ID']
    _client_secret = config['CLIENT_SECRET']
    _url = config['URL_TOKEN']

    def __init__(self):
        self._token_expires_in = 0
        self._token = ''


    def get_new_token(self):
        token_req_payload = {'grant_type': 'client_credentials'}
        resp = requests.post(self._url,
                             data=token_req_payload,
                             verify=True,
                             allow_redirects=False,
                             auth=(self._client_id, self._client_secret))

        token_resp = resp.json()
        self._token = token_resp['access_token']
        self._token_expires_in = token_resp['expires_in']


    def token_is_valid(self):
        return True

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token



