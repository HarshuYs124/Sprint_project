import requests


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, headers=None):
        return requests.get(
            f"{self.base_url}{endpoint}",
            headers=headers
        )

    def post(self, endpoint, payload=None, headers=None):
        return requests.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers
        )

    def delete(self, endpoint, headers=None):
        return requests.delete(
            f"{self.base_url}{endpoint}",
            headers=headers
        )

    def put(self, endpoint, payload=None, headers=None):
        return requests.put(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers
        )
