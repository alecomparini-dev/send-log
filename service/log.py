import requests


class LogService:

    def __init__(self, url, oauth_service):
        self.url = url
        self.oauth_service = oauth_service

    def send_log(self, log, retry = False):
        try:
            response = requests.post(url=self.url, json=log.__dict__, headers=self._config_headers())

            if response.status_code == 401 and not retry:
                self.oauth_service.clean()
                return self.send_log(log, True)

            self._validate_response(log.__dict__, response)

        except Exception as e:
            raise e

    def _validate_response(self, req, resp):
        if 200 <= resp.status_code < 300:
            return True

        print(f'Status:{str(resp.status_code)} - Request:{str(req)} - Response: {str(resp.json())}')
        raise Exception(f'Status:{str(resp.status_code)} - Request:{str(req)} - Response: {str(resp.json())}')

    def _config_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.oauth_service.token
        }
