import requests
import time


class ReqWrapper:
    def __init__(self):
        if not hasattr(type(self), '_session'):
            self.creatSingletonSession()

    @classmethod
    def creatSingletonSession(cls):
        cls.session = requests.Session()

    def get(self, url, **kwargs):
        retry = 5
        while True:
            try:
                return self.session.get(url, **kwargs)
            except requests.ConnectionError as e:
                print('Sessoin get failed, retry:', retry)
                retry -= 1
                if retry < 1:
                    print("Retries end", e)
                    raise e
                time.sleep(2)

    def post(self, url, **kwargs):
        retry = 5
        while True:
            try:
                return self.session.post(url, **kwargs)
            except requests.ConnectionError as e:
                print('Sessoin post failed, retry:', retry)
                retry -= 1
                if retry < 1:
                    print("Retries end", e)
                    raise e
                time.sleep(2)
