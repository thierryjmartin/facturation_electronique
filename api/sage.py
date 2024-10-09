from ..utils.http_client import HttpClient
from ..config import *


class SAGEAPI:
	def __init__(self,
				 sandbox: bool=True,
				 client_id: str='',
				 client_secret: str='',
				 ):
		self.sandbox = sandbox
		self.client_id = client_id or SAGE_CLIENT_ID
		self.client_secret = client_secret or SAGE_CLIENT_SECRET
		self.base_url = SAGE_BASE_URL
		if self.sandbox:
			self.base_url = SAGE_SANDBOX_BASE_URL
		self.client = HttpClient(base_url=self.base_url, api_key='')

	def envoyer_facture(self, facture: dict) -> dict:
		"""
		Envoyer une facture à DPGF
		"""
		response = self.client.post('/factures', json=facture)
		return response.json()
