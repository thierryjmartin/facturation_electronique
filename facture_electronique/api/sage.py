from ..utils.http_client import HttpClient

try:
    from ..config import (
        SAGE_CLIENT_ID,
        SAGE_CLIENT_SECRET,
        SAGE_BASE_URL,
        SAGE_SANDBOX_BASE_URL,
    )
except ImportError:
    from ..template_config import (
        SAGE_CLIENT_ID,
        SAGE_CLIENT_SECRET,
        SAGE_BASE_URL,
        SAGE_SANDBOX_BASE_URL,
    )


class SAGEAPI:
    # SAGE n'a pas encore vraiment d'API...
    def __init__(
        self,
        sandbox: bool = True,
        client_id: str = "",
        client_secret: str = "",
    ):
        self.sandbox = sandbox
        self.client_id = client_id or SAGE_CLIENT_ID
        self.client_secret = client_secret or SAGE_CLIENT_SECRET
        self.base_url = SAGE_BASE_URL
        if self.sandbox:
            self.base_url = SAGE_SANDBOX_BASE_URL
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
