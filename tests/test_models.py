import pytest
from decimal import Decimal
from facture_electronique.models import (
    FactureChorus,
    FactureFacturX,
    ModeDepot,
    Destinataire,
    Fournisseur,
    CadreDeFacturation,
    CodeCadreFacturation,
    References,
    TypeFacture,
    TypeTVA,
    ModePaiement,
    LigneDePoste,
    LigneDeTVA,
    MontantTotal,
    AdressePostale,
    AdresseElectronique,
    SchemeID,
    ConstructeurAdresse,
)


def test_creation_facture_chorus_simple():
    """Teste la création d'une instance simple de FactureChorus et sa sérialisation."""
    facture = FactureChorus(
        mode_depot=ModeDepot.SAISIE_API,
        numero_facture="F-2025-001",
        date_echeance_paiement="2025-11-25",
        destinataire=Destinataire(
            adresse_electronique=AdresseElectronique(identifiant="12345678901234")
        ),
        fournisseur=Fournisseur(
            id_fournisseur=9876,
            adresse_electronique=AdresseElectronique(identifiant="11122233300011"),
        ),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
        ),
        references=References(
            type_facture=TypeFacture.FACTURE,
            type_tva=TypeTVA.SUR_DEBIT,
            mode_paiement=ModePaiement.VIREMENT,
        ),
        montant_total=MontantTotal(
            montant_ht_total=Decimal("100.0"),
            montant_tva=Decimal("20.0"),
            montant_ttc_total=Decimal("120.0"),
            montant_a_payer=Decimal("120.0"),
        ),
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                denomination="Test",
                quantite=Decimal("1"),
                unite="pce",
                montant_unitaire_ht=Decimal("100.0"),
            )
        ],
        lignes_de_tva=[
            LigneDeTVA(
                montant_base_ht=Decimal("100.0"),
                montant_tva=Decimal("20.0"),
                taux_manuel=Decimal("20.0"),
            )
        ],
    )
    assert facture.mode_depot == ModeDepot.SAISIE_API
    assert facture.destinataire.adresse_electronique.identifiant == "12345678901234"


def test_facture_chorus_to_api_payload():
    """Teste la méthode to_api_payload pour la conversion en camelCase."""
    facture = FactureChorus(
        mode_depot=ModeDepot.DEPOT_PDF_API,
        numero_facture="FAC-2024-01",
        date_echeance_paiement="2024-11-25",
        destinataire=Destinataire(
            adresse_electronique=AdresseElectronique(identifiant="12345678901234"),
            code_service_executant="RH",
        ),
        fournisseur=Fournisseur(
            id_fournisseur=9876,
            adresse_electronique=AdresseElectronique(identifiant="11122233300011"),
        ),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
        ),
        references=References(
            type_facture=TypeFacture.FACTURE,
            type_tva=TypeTVA.SUR_DEBIT,
            mode_paiement=ModePaiement.VIREMENT,
        ),
        montant_total=MontantTotal(
            montant_ht_total=Decimal("100.0"),
            montant_tva=Decimal("20.0"),
            montant_ttc_total=Decimal("120.0"),
            montant_a_payer=Decimal("120.0"),
        ),
    )
    payload = facture.to_api_payload()

    assert "modeDepot" in payload
    assert payload["modeDepot"] == "DEPOT_PDF_API"
    assert "numeroFactureSaisi" in payload
    assert "destinataire" in payload
    assert payload["destinataire"]["codeDestinataire"] == "12345678901234"
    assert payload["destinataire"]["codeServiceExecutant"] == "RH"
    assert "fournisseur" in payload
    assert payload["fournisseur"]["idFournisseur"] == 9876
    assert "commentaire" not in payload


def test_creation_facture_facturx():
    """Teste la création d'une instance de FactureFacturX avec les champs requis."""
    facture = FactureFacturX(
        mode_depot=ModeDepot.DEPOT_PDF_API,
        numero_facture="FX-2024-001",
        date_facture="2024-10-18",
        date_echeance_paiement="2024-11-18",
        destinataire=Destinataire(
            adresse_electronique=AdresseElectronique(identifiant="99986401570264"),
            nom="Client Principal SA",
            adresse_postale=AdressePostale(
                ligne_un="123 Rue du Test", code_postal="75001", nom_ville="Paris"
            ),
        ),
        fournisseur=Fournisseur(
            id_fournisseur=12345,
            adresse_electronique=AdresseElectronique(identifiant="26073617692140"),
            nom="Mon Entreprise SAS",
        ),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
        ),
        references=References(
            type_facture=TypeFacture.FACTURE,
            type_tva=TypeTVA.SUR_DEBIT,
            mode_paiement=ModePaiement.VIREMENT,
        ),
        montant_total=MontantTotal(
            montant_ht_total=Decimal("1000.0"),
            montant_tva=Decimal("200.0"),
            montant_ttc_total=Decimal("1200.0"),
            montant_a_payer=Decimal("1200.0"),
        ),
    )
    assert facture.numero_facture == "FX-2024-001"
    assert facture.destinataire.nom == "Client Principal SA"
    assert facture.references.devise_facture == "EUR"  # Vérifie la valeur par défaut


class TestConstructeurAdresse:
    """Teste la classe utilitaire ConstructeurAdresse."""

    def test_construction_siren_simple(self):
        """Vérifie la construction d'une adresse avec seulement un SIREN."""
        adresse = ConstructeurAdresse(siren="123456789").construire()
        assert isinstance(adresse, AdresseElectronique)
        assert adresse.identifiant == "123456789"
        assert adresse.scheme_id == SchemeID.FR_SIREN

    def test_construction_avec_siret(self):
        """Vérifie la construction chaînée avec un SIRET."""
        adresse = (
            ConstructeurAdresse(siren="123456789")
            .avec_siret("12345678901234")
            .construire()
        )
        assert adresse.identifiant == "123456789_12345678901234"

    def test_construction_avec_code_routage(self):
        """Vérifie la construction avec un code de routage."""
        adresse = (
            ConstructeurAdresse(siren="123456789")
            .avec_siret("12345678901234")
            .avec_code_routage("SERVICE01")
            .construire()
        )
        assert adresse.identifiant == "123456789_12345678901234_SERVICE01"

    def test_construction_avec_suffixe(self):
        """Vérifie la construction avec un suffixe."""
        adresse = (
            ConstructeurAdresse(siren="123456789").avec_suffixe("PDP01").construire()
        )
        assert adresse.identifiant == "123456789_PDP01"

    def test_echec_siren_invalide(self):
        """Vérifie qu'une erreur est levée si le SIREN est invalide."""
        with pytest.raises(
            ValueError, match="Le SIREN doit être une chaîne de 9 chiffres."
        ):
            ConstructeurAdresse(siren="12345")
        with pytest.raises(
            ValueError, match="Le SIREN doit être une chaîne de 9 chiffres."
        ):
            ConstructeurAdresse(siren="abcdefghi")

    def test_echec_siret_invalide(self):
        """Vérifie qu'une erreur est levée si le SIRET est invalide."""
        with pytest.raises(
            ValueError, match="Le SIRET doit être une chaîne de 14 chiffres."
        ):
            ConstructeurAdresse(siren="123456789").avec_siret("12345")

    def test_echec_siret_ne_correspond_pas_au_siren(self):
        """Vérifie qu'une erreur est levée si le SIRET ne correspond pas au SIREN."""
        with pytest.raises(
            ValueError, match="Le SIRET ne semble pas correspondre au SIREN de base."
        ):
            ConstructeurAdresse(siren="123456789").avec_siret("98765432101234")

    @pytest.mark.parametrize("code_invalide", ["CODE!", "CODE-AVEC-TIRET"])
    def test_echec_code_routage_invalide(self, code_invalide):
        """Vérifie les erreurs pour un code de routage invalide."""
        with pytest.raises(ValueError, match="caractères alphanumériques"):
            ConstructeurAdresse(siren="123456789").avec_code_routage(code_invalide)
