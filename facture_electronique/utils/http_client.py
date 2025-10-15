import requests


class HttpClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json; charset=UTF-8",
        }

    def get(self, endpoint: str, params=None):
        """
        Effectuer une requête GET
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response

    def post(self, endpoint: str, json=None):
        """
        Effectuer une requête POST
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, json=json, verify=True)
        response.raise_for_status()
        return response
