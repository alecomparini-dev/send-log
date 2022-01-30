import requests


class OAuthService:
    def __init__(self, url, client_id, client_secret):
        self._token = None
        self._url = url
        self._client_id = client_id
        self._client_secret = client_secret

    def _get_new_token(self):
        token_req_payload = {'grant_type': 'client_credentials'}
        resp = requests.post(self._url,
                             data=token_req_payload,
                             verify=True,
                             allow_redirects=False,
                             auth=(self._client_id, self._client_secret))

        token_resp = resp.json()
        return token_resp['access_token']

    @property
    def token(self):
        if not self._token:
            self._token = self._get_new_token()
        return self._token

    def clean(self):
        self._token = None
