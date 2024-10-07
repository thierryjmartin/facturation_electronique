from facturx import generate_facturx_xml, parse_facturx_pdf


def creer_facturx(facture_data: dict, pdf_path: str) -> str:
	"""
	Générer une facture Factur-X à partir de données et d'un PDF
	:return: Chemin vers le fichier PDF Factur-X généré
	"""
	xml_data = generate_facturx_xml(facture_data)
	facturx_pdf = parse_facturx_pdf(pdf_path, xml_data)
	return facturx_pdf
