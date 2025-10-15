from ..utils.http_client import HttpClient

try:
    from ..config import (
        PENNYLANE_CLIENT_ID,
        PENNYLANE_CLIENT_SECRET,
        PENNYLANE_BASE_URL,
        PENNYLANE_SANDBOX_BASE_URL,
    )
except ImportError:
    from ..template_config import (
        PENNYLANE_CLIENT_ID,
        PENNYLANE_CLIENT_SECRET,
        PENNYLANE_BASE_URL,
        PENNYLANE_SANDBOX_BASE_URL,
    )


class PennylaneAPI:
    def __init__(
        self,
        sandbox: bool = True,
        client_id: str = "",
        client_secret: str = "",
    ):
        self.sandbox = sandbox
        self.client_id = client_id or PENNYLANE_CLIENT_ID
        self.client_secret = client_secret or PENNYLANE_CLIENT_SECRET
        self.base_url = PENNYLANE_BASE_URL
        if self.sandbox:
            self.base_url = PENNYLANE_SANDBOX_BASE_URL
        self.client = HttpClient(base_url=self.base_url, api_key="")

    def get_token(self):
        # GET https://www.sageone.com/oauth2/auth/central?filter=apiv3.1&response_type=code&client_id=4b6xxxxxxx710&redirect_uri=https://myapp.com/auth/callback&scope=full_access&state=random_string
        pass

    def envoyer_facture(self, facture: dict) -> dict:
        """
        Envoyer une facture à Pennylane
        """
        response = self.client.post("/factures", json=facture)
        return response.json()
