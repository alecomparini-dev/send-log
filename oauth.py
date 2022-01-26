import jwt
import requests
from datetime import datetime
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
        self._token_expires_in = jwt.decode(self._token, options={"verify_signature": False})['exp']

    def token_is_valid(self):
        if (self._token_expires_in - datetime.now().timestamp()) <= 0:
            self.get_new_token()

    @property
    def token(self):
        self.token_is_valid()
        return self._token
