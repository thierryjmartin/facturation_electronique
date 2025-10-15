import os

from ..utils.http_client import HttpClient
from ..exceptions import ErreurConfiguration


class SAGEAPI:
    BASE_URL = ""
    SANDBOX_BASE_URL = ""

    # SAGE n'a pas encore vraiment d'API...
    def __init__(
        self,
        sandbox: bool = True,
        client_id: str = "",
        client_secret: str = "",
    ):
        self.sandbox = sandbox
        self.client_id = client_id or os.getenv("SAGE_CLIENT_ID")
        if not self.client_id:
            raise ErreurConfiguration("SAGE_CLIENT_ID")

        self.client_secret = client_secret or os.getenv("SAGE_CLIENT_SECRET")
        if not self.client_secret:
            raise ErreurConfiguration("SAGE_CLIENT_SECRET")

        self.base_url = self.BASE_URL
        if self.sandbox:
            self.base_url = self.SANDBOX_BASE_URL
        self.client = HttpClient(base_url=self.base_url, api_key="")

    def get_token(self):
        # GET https://www.sageone.com/oauth2/auth/central?filter=apiv3.1&response_type=code&client_id=4b6xxxxxxx710&redirect_uri=https://myapp.com/auth/callback&scope=full_access&state=random_string
        pass

    def envoyer_facture(self, facture: dict) -> dict:
        """
        Envoyer une facture à SAGE
        """
        response = self.client.post("/factures", json=facture)
        return response.json()
