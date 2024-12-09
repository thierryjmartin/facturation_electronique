if __name__ == '__main__':
	from facture_electronique.api.chorus_pro import ChorusProAPI
	c = ChorusProAPI()
	# print(c.token)

	"""
	 A titre d'exemple, voici une cinématique nominale pour avoir des informations sur une structure et ses services:

              1- Faire appel à l'API "RechercherStructure" afin de retrouver des structures avec quelques informations en sortie notamment "idStructureCPP

              2- Faire appel à l'API "ConsulterStructure" avec en entrée l'idStructureCPP pour avoir les paramètres obligatoires de la structure (numéro d'engagement et/ou code service)

              3- Faire appel à l'API "rechercherServicesStructure" avec "idStructure" en entrée de la requête afin de visualiser les services actifs de la structure renseignée

              4- Faire appel à l'API consulterServiceStructure avec idService en entrée de la requête afin de consulter les paramètres obligatoires du service.
    """

	# 1 .

	payload={
			  "parametres": {
				"nbResultatsParPage": 10,
				"pageResultatDemandee": 1,
				"triColonne": "IdentifiantStructure",
				"triSens": "Descendant"
			  },
			  "restreindreStructuresPrivees": False,
			  "structure": {
				#"adresseCodePays": "string",
				#"adresseCodePostal": "string",
				#"adresseVille": "string",
				#"estMOA": true,
				#"estMOAUniquement": true,
				"identifiantStructure": "26073617692140",
				#"libelleStructure": "string",
				#"nomStructure": "string",
				#"prenomStructure": "string",
				#"raisonSocialeStructure": "string",
				#"statutStructure": "ACTIF",
				"typeIdentifiantStructure": "SIRET",
				#"typeStructure": "PUBLIQUE"
			  }
			}

	#recherche_structure = c.rechercher_structure(payload)

	#identifiant_cpro = 0
	#if recherche_structure["parametresRetour"]["total"] == 1:
	#	identifiant_cpro = recherche_structure["listeStructures"][0]["idStructureCPP"]
	#print(identifiant_cpro)

	# identifiant_cpro = 12345

	# identifiant_cpro = c.obtenir_identifiant_cpro_depuis_siret("26073617692140")

	# 2 .
	# c.consulter_structure(26300989)
	# 3 .
	# c.rechercher_services_structure(26300989)

	# 4.
	service = c.consulter_service_structure(id_structure=26311042, id_service=10657669)
	print(service)

	# exemple_facture = {
	# 					  "cadreDeFacturation": {
	# 						"codeCadreFacturation": "A1_FACTURE_FOURNISSEUR",
	# 						"codeServiceValideur": "string",
	# 						"codeStructureValideur": "string"
	# 					  },
	# 					  "commentaire": "string",
	# 					  "dateFacture": "2024-10-08T11:30:23.463Z",
	# 					  "destinataire": {
	# 						"codeDestinataire": "string",
	# 						"codeServiceExecutant": "string"
	# 					  },
	# 					  "fournisseur": {
	# 						"codeCoordonneesBancairesFournisseur": 0,
	# 						"idFournisseur": "26073617692140",
	# 						"idServiceFournisseur": "SERVICE_PRIVE_1_26073617692140",
	# 					  },
	# 					  "idUtilisateurCourant": 0,
	# 					  "lignePoste": [
	# 						{
	# 						  "lignePosteDenomination": "string",
	# 						  "lignePosteMontantRemiseHT": 0,
	# 						  "lignePosteMontantUnitaireHT": 0,
	# 						  "lignePosteNumero": 0,
	# 						  "lignePosteQuantite": 0,
	# 						  "lignePosteReference": "string",
	# 						  "lignePosteTauxTva": "string",
	# 						  "lignePosteTauxTvaManuel": 0,
	# 						  "lignePosteUnite": "string"
	# 						}
	# 					  ],
	# 					  "ligneTva": [
	# 						{
	# 						  "ligneTvaMontantBaseHtParTaux": 0,
	# 						  "ligneTvaMontantTvaParTaux": 0,
	# 						  "ligneTvaTaux": "string",
	# 						  "ligneTvaTauxManuel": 0
	# 						}
	# 					  ],
	# 					  "modeDepot": "SAISIE_API",
	# 					  "montantTotal": {
	# 						"montantAPayer": 0,
	# 						"montantHtTotal": 0,
	# 						"montantRemiseGlobaleTTC": 0,
	# 						"montantTVA": 0,
	# 						"montantTtcTotal": 0,
	# 						"motifRemiseGlobaleTTC": "string"
	# 					  },
	# 					  "numeroFactureSaisi": "string",
	# 					  "pieceJointeComplementaire": [
	# 						{
	# 						  "pieceJointeComplementaireDesignation": "string",
	# 						  "pieceJointeComplementaireId": 0,
	# 						  "pieceJointeComplementaireIdLiaison": 0,
	# 						  "pieceJointeComplementaireNumeroLigneFacture": 0,
	# 						  "pieceJointeComplementaireType": "string"
	# 						}
	# 					  ],
	# 					  "pieceJointePrincipale": [
	# 						{
	# 						  "pieceJointePrincipaleDesignation": "string",
	# 						  "pieceJointePrincipaleId": 0
	# 						}
	# 					  ],
	# 					  "references": {
	# 						"deviseFacture": "string",
	# 						"modePaiement": "CHEQUE",
	# 						"motifExonerationTva": "string",
	# 						"numeroBonCommande": "string",
	# 						"numeroFactureOrigine": "string",
	# 						"numeroMarche": "string",
	# 						"typeFacture": "AVOIR",
	# 						"typeTva": "TVA_SUR_DEBIT"
	# 					  }
	# 					}

	# exemple_facture = {
	# 	"modeDepot": "SAISIE_API",
	# 	"numeroFactureSaisi": None,
	#
	# 	"destinataire": {
	# 		"codeDestinataire": "99986401570264", # SIRET  trouvé via une recherche...
	# 		#"codeServiceExecutant": "DIRINFRA"
	# 	},
	# 	"fournisseur": {
	# 		# j'ai retrouvé ce code en faisant une recherche de fournisseur..., j'aurais pu chercher par siret ?
	# 		# le SIRET de mon fournisseur 26073617692140
	# 		"idFournisseur": 26300989,
	# 		#"typeIdentifiantFournisseur": "SIRET",
	# 	#	"idServiceFournisseur": 26073617692140,
	# 	#	"codeCoordonneesBancairesFournisseur": 132
	# 	},
	# 	"cadreDeFacturation": {
	# 		"codeCadreFacturation": "A1_FACTURE_FOURNISSEUR",
	# 		"codeStructureValideur": None
	# 	},
	# 	"references": {
	# 		"deviseFacture": "EUR",
	# 		"typeFacture": "FACTURE",
	# 		"typeTva": "TVA_SUR_DEBIT",
	# 		"motifExonerationTva": None,
	# 		"numeroMarche": "VABFM001",
	# 		"numeroBonCommande": None,
	# 		"numeroFactureOrigine": None,
	# 		"modePaiement": "ESPECE"
	# 	},
	# 	"lignePoste": [
	# 		{
	# 			"lignePosteNumero": 1,
	# 			"lignePosteReference": "R1",
	# 			"lignePosteDenomination": "D1",
	# 			"lignePosteQuantite": 10,
	# 			"lignePosteUnite": "lot",
	# 			"lignePosteMontantUnitaireHT": 50.000000,
	# 			"lignePosteMontantRemiseHT": None,
	# 			#"lignePosteTauxTva": "TVA5",
	# 			"lignePosteTauxTva": None,
	# 			#"lignePosteTauxTvaManuel": None
	# 			"lignePosteTauxTvaManuel": 20
	# 		}
	# 		, {
	# 			"lignePosteNumero": 2,
	# 			"lignePosteReference": "R2",
	# 			"lignePosteDenomination": "D2",
	# 			"lignePosteQuantite": 12,
	# 			"lignePosteUnite": "Kg",
	# 			"lignePosteMontantUnitaireHT": 36.000000,
	# 			"lignePosteMontantRemiseHT": None,
	# 			"lignePosteTauxTva": None,
	# 			"lignePosteTauxTvaManuel": 2.1
	# 		}
	# 		, {
	# 			"lignePosteNumero": 3,
	# 			"lignePosteReference": "R3",
	# 			"lignePosteDenomination": "D3",
	# 			"lignePosteQuantite": 16,
	# 			"lignePosteUnite": "lot",
	# 			"lignePosteMontantUnitaireHT": 24.000000,
	# 			"lignePosteMontantRemiseHT": None,
	# 			"lignePosteTauxTva": None,
	# 			"lignePosteTauxTvaManuel": 5
	# 		}
	# 		, {
	# 			"lignePosteNumero": 4,
	# 			"lignePosteReference": "XX",
	# 			"lignePosteDenomination": "XX",
	# 			"lignePosteQuantite": 1,
	# 			"lignePosteUnite": "lot",
	# 			"lignePosteMontantUnitaireHT": 10.000000,
	# 			"lignePosteMontantRemiseHT": None,
	# 			#"lignePosteTauxTva": "TVA5",
	# 			"lignePosteTauxTva": None,
	# 			#"lignePosteTauxTvaManuel": None
	# 			"lignePosteTauxTvaManuel": 20
	# 		}
	# 	],
	# 	"ligneTva": [
	# 		{
	# 			#"ligneTvaTauxManuel": None,
	# 			#"ligneTvaTaux": "TVA5",
	# 			"ligneTvaTauxManuel": 20,
	# 			"ligneTvaTaux": None,
	# 			"ligneTvaMontantBaseHtParTaux": 510.000000,
	# 			"ligneTvaMontantTvaParTaux": 102.000000
	# 		},
	# 		{
	# 			"ligneTvaTauxManuel": 2.1,
	# 			"ligneTvaTaux": None,
	# 			"ligneTvaMontantBaseHtParTaux": 432.000000,
	# 			"ligneTvaMontantTvaParTaux": 9.072000
	# 		}
	# 		, {
	# 			"ligneTvaTauxManuel": 5,
	# 			"ligneTvaTaux": None,
	# 			"ligneTvaMontantBaseHtParTaux": 384.000000,
	# 			"ligneTvaMontantTvaParTaux": 19.200000
	# 		}
	# 	],
	# 	"montantTotal": {
	# 		"montantHtTotal": 1326.000000,
	# 		"montantTVA": 130.272000,
	# 		"montantTtcTotal": 1406.272000,
	# 		"montantRemiseGlobaleTTC": 50.000000,
	# 		"motifRemiseGlobaleTTC": "Geste commercial",
	# 		"montantAPayer": 1400.000000
	# 	},
	# 	"commentaire": "Création_VABF_SoumettreFacture"
	# }

	from ..models import *

	exemple_facture_mode_api = Facture(
		mode_depot=ModeDepot("SAISIE_API"),
		# numero_facture_saisi="20240000000000000013", # ce champ n'est pas utilié en mode_depot saisie_api
		#date_facture="2024-15-08", # seulement en depot PDF
		id_utilisateur_courant=0,
		destinataire=Destinataire(
			code_destinataire="99986401570264",
			code_service_executant='' # est absent
		),
		fournisseur=Fournisseur(
			id_fournisseur=12345, # identifiant_cpro,
			# Les autres champs du fournisseur sont absents
		),
		cadre_de_facturation=CadreDeFacturation(
			code_cadre_facturation="A1_FACTURE_FOURNISSEUR",
			code_structure_valideur=None
		),
		references=References(
			devise_facture="EUR",
			type_facture=TypeFacture("FACTURE"),
			type_tva=TypeTVA("TVA_SUR_DEBIT"),
			motif_exoneration_tva=None,
			numero_marche="VABFM001",
			numero_bon_commande=None,
			numero_facture_origine=None,
			mode_paiement=ModePaiement("ESPECE")
		),
		ligne_poste=[
			LignePoste(
				ligne_poste_numero=1,
				ligne_poste_reference="R1",
				ligne_poste_denomination="D1",
				ligne_poste_quantite=10,
				ligne_poste_unite="lot",
				ligne_poste_montant_unitaire_HT=50.00,
				ligne_poste_montant_remise_HT=0,
				ligne_poste_taux_tva='',
				ligne_poste_taux_tva_manuel=20
			),
			LignePoste(
				ligne_poste_numero=2,
				ligne_poste_reference="R2",
				ligne_poste_denomination="D2",
				ligne_poste_quantite=12,
				ligne_poste_unite="Kg",
				ligne_poste_montant_unitaire_HT=36.00,
				ligne_poste_montant_remise_HT=0,
				ligne_poste_taux_tva='',
				ligne_poste_taux_tva_manuel=2.1
			),
			LignePoste(
				ligne_poste_numero=3,
				ligne_poste_reference="R3",
				ligne_poste_denomination="D3",
				ligne_poste_quantite=16,
				ligne_poste_unite="lot",
				ligne_poste_montant_unitaire_HT=24.00,
				ligne_poste_montant_remise_HT=0,
				ligne_poste_taux_tva='',
				ligne_poste_taux_tva_manuel=5
			),
			LignePoste(
				ligne_poste_numero=4,
				ligne_poste_reference="XX",
				ligne_poste_denomination="XX",
				ligne_poste_quantite=1,
				ligne_poste_unite="lot",
				ligne_poste_montant_unitaire_HT=10.00,
				ligne_poste_montant_remise_HT=0,
				ligne_poste_taux_tva='',
				ligne_poste_taux_tva_manuel=20
			)
		],
		ligne_tva=[
			LigneTva(
				ligne_tva_taux_manuel=20,
				ligne_tva_taux=None,
				ligne_tva_montant_base_ht_par_taux=510.00,
				ligne_tva_montant_tva_par_taux=102.00
			),
			LigneTva(
				ligne_tva_taux_manuel=2.1,
				ligne_tva_taux=None,
				ligne_tva_montant_base_ht_par_taux=432.00,
				ligne_tva_montant_tva_par_taux=9.072
			),
			LigneTva(
				ligne_tva_taux_manuel=5,
				ligne_tva_taux=None,
				ligne_tva_montant_base_ht_par_taux=384.00,
				ligne_tva_montant_tva_par_taux=19.20
			)
		],
		montant_total=MontantTotal(
			montant_ht_total=1326.00,
			montant_TVA=130.272,
			montant_ttc_total=1406.272,
			montant_remise_globale_TTC=50.00,
			motif_remise_globale_TTC="Geste commercial",
			montant_a_payer=1400.00
		),
		commentaire="Création_VABF_SoumettreFacture"
	)


	# c.envoyer_facture(exemple_facture_mode_api.to_chorus_pro_payload())
	# print(exemple_facture.to_facturx_basic())

	from ..utils.files import *
	file_path = get_absolute_path("facture_electronique/exemples/dummy.pdf")

	file_path_pdfa = get_absolute_path("facture_electronique/exemples/dummy.pdfa.pdf")
	from ..utils.pdfs import convert_to_pdfa, sign_pdf
	convert_to_pdfa(file_path, file_path_pdfa)

	exemple_facture_mode_pdf = Facture(
		mode_depot=ModeDepot("DEPOT_PDF_API"),
		numero_facture_saisi="20240000000000000110", # ce champ n'est pas utilisé en mode_depot saisie_api
		date_facture="2024-10-18", # seulement en depot PDF
		date_echeance_paiement="2014-12-18",
		id_utilisateur_courant=0,
		piece_jointe_principale = [PieceJointePrincipale(
			piece_jointe_principale_designation = 'facture',
			# piece_jointe_principale_id = pj_id
		)],
		destinataire=Destinataire(
			nom="acheteur 99986401570264",
			code_destinataire="99986401570264",
			adresse_postale=AdressePostale(
				code_postal='122345',
				ligne_un='adresse du destinataire',
				nom_ville='PARIS',
				pays_code_iso='FR',
			),
			code_service_executant='',
		),
		fournisseur=Fournisseur(
			id_fournisseur= 12345, #identifiant_cpro,
			nom='Fournisseur 26073617692140',
			siret='26073617692140',
			numero_tva_intra='FR61529571234',
			adresse_postale=AdressePostale(
				code_postal='122345',
				ligne_un='2 rue de l andouillette',
				nom_ville='PARIS',
				pays_code_iso='FR',
			)
			# Les autres champs du fournisseur sont absents
		),
		cadre_de_facturation=CadreDeFacturation(
			code_cadre_facturation=CodeCadreFacturation("A1_FACTURE_FOURNISSEUR"),
			code_structure_valideur=None
		),
		references=References(
			devise_facture="EUR",
			type_facture=TypeFacture("FACTURE"),
			type_tva=TypeTVA("TVA_SUR_DEBIT"),
			motif_exoneration_tva=None,
			numero_marche="VABFM001",
			numero_bon_commande="coucou",
			numero_facture_origine=None,
			mode_paiement=ModePaiement("ESPECE")
		),
		montant_total=MontantTotal(
			montant_ht_total=1326.00,
			montant_TVA=130.272,
			montant_ttc_total=1456.272,
			montant_remise_globale_TTC=0.00,
			motif_remise_globale_TTC="",
			acompte=56.272,
			montant_a_payer=1400.00
		),
		commentaire = 'voici mon commentaire',
		ligne_poste=[
			LignePoste(
				ligne_poste_numero=1,
				ligne_poste_reference="R1",
				ligne_poste_denomination="D1",
				ligne_poste_quantite=10,
				ligne_poste_unite="lot",
				ligne_poste_montant_unitaire_HT=50.00,
				ligne_poste_montant_remise_HT=5,
				ligne_poste_taux_tva='',
				ligne_poste_taux_tva_manuel=20,
				ligne_poste_tva_categorie = TvaCategories('S'),
				ligne_poste_code_raison_reduction='parce que je suis sympa'
			),
			LignePoste(
				ligne_poste_numero=2,
				ligne_poste_reference="R2",
				ligne_poste_denomination="D2",
				ligne_poste_quantite=12,
				ligne_poste_unite="Kg",
				ligne_poste_montant_unitaire_HT=36.00,
				ligne_poste_montant_remise_HT=0,
				ligne_poste_taux_tva='',
				ligne_poste_taux_tva_manuel=2.1,
				ligne_poste_tva_categorie = TvaCategories('S')
			),
			LignePoste(
				ligne_poste_numero=3,
				ligne_poste_reference="R3",
				ligne_poste_denomination="D3",
				ligne_poste_quantite=16,
				ligne_poste_unite="lot",
				ligne_poste_montant_unitaire_HT=24.00,
				ligne_poste_montant_remise_HT=0,
				ligne_poste_taux_tva='',
				ligne_poste_taux_tva_manuel=5,
				ligne_poste_tva_categorie = TvaCategories('S')
			),
			LignePoste(
				ligne_poste_numero=4,
				ligne_poste_reference="XX",
				ligne_poste_denomination="XX",
				ligne_poste_quantite=1,
				ligne_poste_unite="lot",
				ligne_poste_montant_unitaire_HT=10.00,
				ligne_poste_montant_remise_HT=0,
				ligne_poste_taux_tva='',
				ligne_poste_taux_tva_manuel=20,
				ligne_poste_tva_categorie = TvaCategories('S')
			)
		],
		ligne_tva=[
			LigneTva(
				ligne_tva_taux_manuel=20,
				ligne_tva_taux=None,
				ligne_tva_montant_base_ht_par_taux=510.00,
				ligne_tva_montant_tva_par_taux=102.00,
				ligne_tva_categorie=TvaCategories('S')
			),
			LigneTva(
				ligne_tva_taux_manuel=2.1,
				ligne_tva_taux=None,
				ligne_tva_montant_base_ht_par_taux=432.00,
				ligne_tva_montant_tva_par_taux=9.072,
				ligne_tva_categorie=TvaCategories('S')
			),
			LigneTva(
				ligne_tva_taux_manuel=5,
				ligne_tva_taux=None,
				ligne_tva_montant_base_ht_par_taux=384.00,
				ligne_tva_montant_tva_par_taux=19.20,
				ligne_tva_categorie=TvaCategories('S')
			)
		],
	)

	import facturx
	from ..utils.facturx import (
		gen_xml_depuis_facture,
		valider_xml_xldt,
		chemin_xldt_basic,
		chemin_xldt_minimum,
		chemin_xldt_en16931
	)

	file_path_facturx_mini = file_path + '.facturx.minmum.pdf'
	file_path_facturx_basic = file_path + '.facturx.basic.pdf'
	file_path_facturx_en16931 = file_path + '.facturx.en16931.pdf'

	# test generation factur-x minimum
	xml = gen_xml_depuis_facture(exemple_facture_mode_pdf.to_facturx_minimum())
	valider_xml_xldt(xml, chemin_xldt_minimum)
	facturx.generate_from_file(
		file_path_pdfa,
		xml,
		output_pdf_file=file_path_facturx_mini,
		flavor='factur-x',
		level='minimum',
		check_xsd=False,
	)
	facturx.generate_from_file(
		file_path_pdfa,
		xml,
		output_pdf_file=file_path_facturx_mini,
		flavor='factur-x',
		level='minimum',
		check_xsd=True,
	)

	# test generation factur-x basic
	xml = gen_xml_depuis_facture(exemple_facture_mode_pdf.to_facturx_basic())
	valider_xml_xldt(xml, chemin_xldt_basic)
	facturx.generate_from_file(
		file_path_pdfa,
		xml,
		output_pdf_file=file_path_facturx_basic,
		flavor='factur-x',
		level='basic',
		check_xsd=False,
	)
	facturx.generate_from_file(
		file_path_pdfa,
		xml,
		output_pdf_file=file_path_facturx_basic,
		flavor='factur-x',
		level='basic',
		check_xsd=True,
	)

	# test generation factur-x EN16931
	xml = gen_xml_depuis_facture(exemple_facture_mode_pdf.to_facturx_en16931())
	valider_xml_xldt(xml, chemin_xldt_en16931)
	facturx.generate_from_file(
		file_path_pdfa,
		xml,
		output_pdf_file=file_path_facturx_en16931,
		flavor='factur-x',
		level='en16931',
		check_xsd=False,
	)
	facturx.generate_from_file(
		file_path_pdfa,
		xml,
		output_pdf_file=file_path_facturx_en16931,
		flavor='factur-x',
		level='en16931',
		check_xsd=True
	)

	# besoin d'un certificat pour cela
	# https://learn.microsoft.com/en-us/azure/iot-hub/reference-x509-certificates
	# pour faire un factur-x, il faudra un eseal...
	try:
		# l'ajout de la signature fait sauter la conformité PDF/A
		file_path_pdfsigned = file_path + '.pdfsigned.pdf'
		sign_pdf(
			file_path_facturx_en16931,
			file_path_pdfsigned,
			get_absolute_path("facture_electronique/exemples/key.key"),
			get_absolute_path("facture_electronique/exemples/cert.cert"),
			tuple(),
		)
		file_path_pdfsigned_pdfa = file_path + '.pdfsigned.pdfa.pdf'
		# la conversion en PDF/A fait sauter les signatures
		convert_to_pdfa(file_path_pdfsigned, file_path_pdfsigned_pdfa)
	except AttributeError:
		# AttributeError est généré si les fichiers de clé et/ou certificat n'existent pas
		pass

	# test envoi faxctur-x basic vers chorus pro en mod pdf.
	# reponse_fichier = c.ajouter_fichier_dans_systeme(
	# 	file_to_base64(file_path_facturx_basic),
	# 	"facture.pdf",
	# 	guess_mime_type(file_path),
	# 	get_file_extension(file_path),
	# )
	#
	# pj_id = reponse_fichier["pieceJointeId"]
	#
	# exemple_facture_mode_pdf.piece_jointe_principale[0].piece_jointe_principale_id = pj_id
	#
	# reponse_envoi_facture = c.envoyer_facture(exemple_facture_mode_pdf.to_chorus_pro_payload())
	#
	# id_facture_cpro = reponse_envoi_facture['identifiantFactureCPP']
	#
	# c.obtenir_statut_facture(id_facture_cpro)



