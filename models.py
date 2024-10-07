from pydantic import BaseModel

class Facture(BaseModel):
	facture_id: str
	date: str
	client: dict
	montant_total: float
	# Autres champs pertinents
