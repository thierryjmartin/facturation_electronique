from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from decimal import Decimal
from typing import List, Optional, Annotated, Dict, Any

from .utils.strings_and_dicts import to_camel_case, nettoyer_dict
from .utils.datetime_utils import obtenir_date_iso_maintenant
from .utils.facturx import ProfilFacturX
from .constructeur import ConstructeurFacturX

FRENCH_CAMEL_CASE_CONFIG = ConfigDict(
    alias_generator=to_camel_case,
    populate_by_name=True,
    use_enum_values=True,
)


class CodeCadreFacturation(str, Enum):
    A1_FACTURE_FOURNISSEUR = "A1_FACTURE_FOURNISSEUR"
    A2_FACTURE_FOURNISSEUR_DEJA_PAYEE = "A2_FACTURE_FOURNISSEUR_DEJA_PAYEE"
    A9_FACTURE_SOUSTRAITANT = "A9_FACTURE_SOUSTRAITANT"
    A12_FACTURE_COTRAITANT = "A12_FACTURE_COTRAITANT"


class CadreDeFacturation(BaseModel):
    """Définit le cadre de facturation (ex: A1 pour une facture fournisseur)."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    code_cadre_facturation: CodeCadreFacturation
    code_service_valideur: Optional[str] = None
    code_structure_valideur: Optional[str] = None


class AdressePostale(BaseModel):
    """Représente une adresse postale."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    code_postal: Optional[str] = None
    ligne_un: Optional[str] = None
    ligne_deux: Optional[str] = None
    nom_ville: Optional[str] = None
    pays_code_iso: Optional[str] = "FR"


class Destinataire(BaseModel):
    """Informations sur le destinataire de la facture (le client)."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    code_destinataire: str  # SIRET
    code_service_executant: Optional[str] = None
    nom: Optional[str] = None
    adresse_postale: Optional[AdressePostale] = None


class Fournisseur(BaseModel):
    """Informations sur le fournisseur qui émet la facture."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    id_fournisseur: int  # Identifiant Chorus Pro
    code_coordonnees_bancaires_fournisseur: Optional[int] = None
    id_service_fournisseur: Optional[int] = None
    nom: Optional[str] = None
    siret: Optional[str] = None
    numero_tva_intra: Optional[str] = None
    iban: Optional[str] = None
    adresse_postale: Optional[AdressePostale] = None


class CategorieTVA(str, Enum):
    """Catégories de TVA standardisées pour Factur-X."""

    STANDARD = "S"
    ZERO = "Z"
    EXONEREE = "E"
    AUTO_LIQUIDATION = "AE"
    INTRA_COMMUNAUTAIRE = "K"
    EXPORT = "G"
    HORS_CHAMP = "O"
    CANARIES = "L"
    CEUTA_MELILLA = "M"


class CodeRaisonReduction(str, Enum):
    """Codes standardisés pour justifier une réduction ou une charge."""

    REMISE_PUBLICITAIRE = "AA"
    SUPPLEMENT_EMBALLAGE = "ABL"
    AUTRES_SERVICES = "ADR"
    ENLEVEMENT = "ADT"
    COUTS_TRANSPORT = "FC"
    FRAIS_FINANCIERS = "FI"
    ETIQUETAGE = "LA"


class LigneDePoste(BaseModel):
    """Représente une ligne de détail dans une facture."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    numero: int
    reference: Optional[str] = None
    denomination: str
    quantite: Annotated[
        Decimal,
        Field(
            gt=0,
            max_digits=12,
            decimal_places=4,
            description="Quantité facturée pour cette ligne.",
        ),
    ]
    unite: str
    montant_unitaire_ht: Annotated[
        Decimal,
        Field(
            gt=0,
            max_digits=12,
            decimal_places=4,
            description="Montant unitaire Hors Taxes de l'article.",
        ),
    ]
    montant_remise_ht: Optional[
        Annotated[
            Decimal,
            Field(
                ge=0,
                max_digits=12,
                decimal_places=4,
                description="Montant de la remise HT.",
            ),
        ]
    ] = None
    taux_tva: Optional[str] = None  # Ex: "TVA20"
    taux_tva_manuel: Optional[
        Annotated[
            Decimal,
            Field(
                ge=0,
                max_digits=12,
                decimal_places=4,
                description="Taux de TVA avec valeur manuelle.",
            ),
        ]
    ] = None
    categorie_tva: Optional[CategorieTVA] = None
    date_debut_periode: Optional[str] = None
    date_fin_periode: Optional[str] = None
    code_raison_reduction: Optional[CodeRaisonReduction] = None
    raison_reduction: Optional[str] = None


class LigneDeTVA(BaseModel):
    """Représente une ligne de totalisation par taux de TVA."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    montant_base_ht: Annotated[
        Decimal,
        Field(
            ge=0,
            max_digits=12,
            decimal_places=4,
            description="Montant de la base HT pour cette ligne de TVA.",
        ),
    ]
    montant_tva: Annotated[
        Decimal,
        Field(
            ge=0,
            max_digits=12,
            decimal_places=4,
            description="Montant de la TVA pour cette ligne.",
        ),
    ]
    taux: Optional[str] = None
    taux_manuel: Annotated[
        Decimal,
        Field(
            ge=0,
            max_digits=12,
            decimal_places=4,
            description="Taux de TVA avec valeur manuelle.",
        ),
    ] = None
    categorie: Optional[CategorieTVA] = None


class MontantTotal(BaseModel):
    """Contient tous les montants totaux de la facture."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    montant_ht_total: Annotated[
        Decimal,
        Field(ge=0, max_digits=12, decimal_places=4, description="Montant total HT."),
    ]
    montant_tva: Annotated[
        Decimal,
        Field(
            ge=0,
            max_digits=12,
            decimal_places=4,
            description="Montant total de la TVA.",
        ),
    ]
    montant_ttc_total: Annotated[
        Decimal,
        Field(ge=0, max_digits=12, decimal_places=4, description="Montant total TTC."),
    ]
    montant_a_payer: Annotated[
        Decimal,
        Field(ge=0, max_digits=12, decimal_places=4, description="Montant à payer."),
    ]
    acompte: Optional[
        Annotated[
            Decimal,
            Field(ge=0, max_digits=12, decimal_places=4, description="Acompte versé."),
        ]
    ] = None
    montant_remise_globale_ttc: Optional[
        Annotated[
            Decimal,
            Field(
                ge=0,
                max_digits=12,
                decimal_places=4,
                description="Montant de la remise globale TTC.",
            ),
        ]
    ] = None
    motif_remise_globale_ttc: Optional[str] = None


class PieceJointeComplementaire(BaseModel):
    """Représente une pièce jointe complémentaire."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    designation: str
    id: int
    id_liaison: int
    numero_ligne_facture: int
    type: str


class PieceJointePrincipale(BaseModel):
    """Représente la pièce jointe principale (la facture PDF elle-même)."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    designation: str
    id: Optional[int] = None


class ModePaiement(str, Enum):
    """Modes de paiement acceptés."""

    CHEQUE = "CHEQUE"
    PRELEVEMENT = "PRELEVEMENT"
    VIREMENT = "VIREMENT"
    ESPECE = "ESPECE"
    AUTRE = "AUTRE"
    REPORT = "REPORT"


class TypeFacture(str, Enum):
    """Type de document (facture ou avoir)."""

    FACTURE = "FACTURE"
    AVOIR = "AVOIR"


class TypeTVA(str, Enum):
    """Régime de TVA."""

    SUR_DEBIT = "TVA_SUR_DEBIT"
    SUR_ENCAISSEMENT = "TVA_SUR_ENCAISSEMENT"
    EXONERATION = "EXONERATION"
    SANS_TVA = "SANS_TVA"


class References(BaseModel):
    """Contient les références diverses de la facture (devise, type, etc.)."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    devise_facture: str = "EUR"
    mode_paiement: ModePaiement
    type_facture: TypeFacture
    type_tva: TypeTVA
    numero_marche: Optional[str] = None
    motif_exoneration_tva: Optional[str] = None
    numero_bon_commande: Optional[str] = None
    numero_facture_origine: Optional[str] = None


class ModeDepot(str, Enum):
    """Mode de dépôt de la facture sur Chorus Pro."""

    SAISIE_API = "SAISIE_API"
    DEPOT_PDF_API = "DEPOT_PDF_API"
    DEPOT_PDF_SIGNE_API = "DEPOT_PDF_SIGNE_API"


# --- Modèles de base ---


class FactureBase(BaseModel):
    """Modèle de base contenant les champs communs à toutes les factures."""

    model_config = FRENCH_CAMEL_CASE_CONFIG
    date_facture: str = Field(default_factory=obtenir_date_iso_maintenant)
    mode_depot: ModeDepot
    destinataire: Destinataire
    fournisseur: Fournisseur
    cadre_de_facturation: CadreDeFacturation
    references: References
    montant_total: MontantTotal
    lignes_de_poste: List[LigneDePoste] = Field(default_factory=list)
    lignes_de_tva: List[LigneDeTVA] = Field(default_factory=list)
    commentaire: Optional[str] = None
    id_utilisateur_courant: Optional[int] = 0
    pieces_jointes_complementaires: Optional[List[PieceJointeComplementaire]] = None


# --- Modèle pour l'API Chorus Pro ---


class FactureChorus(FactureBase):
    """Modèle spécifique pour une soumission à l'API Chorus Pro."""

    numero_facture_saisi: Optional[str] = None
    pieces_jointes_principales: Optional[List[PieceJointePrincipale]] = None

    def to_api_payload(self) -> Dict[str, Any]:
        """
        Convertit le modèle interne Pydantic en payload JSON conforme à l'API Chorus Pro.
        Corrige la casse, les noms de champs, et supprime les données interdites.
        """

        # Base minimale du payload
        payload = {
            "numeroFactureSaisi": self.numero_facture_saisi,
            "modeDepot": self.mode_depot,
            "destinataire": {
                "codeDestinataire": self.destinataire.code_destinataire,
                "codeServiceExecutant": self.destinataire.code_service_executant or "",
            },
            "fournisseur": {
                "idFournisseur": self.fournisseur.id_fournisseur,
            },
            "cadreDeFacturation": {
                "codeCadreFacturation": self.cadre_de_facturation.code_cadre_facturation,
            },
            "references": {
                "deviseFacture": self.references.devise_facture,
                "modePaiement": self.references.mode_paiement,
                "typeFacture": self.references.type_facture,
                "typeTva": self.references.type_tva,
                "numeroMarche": self.references.numero_marche,
            },
            "commentaire": self.commentaire,
            "idUtilisateurCourant": self.id_utilisateur_courant or 0,
        }

        # --- Fournisseur : champs optionnels
        if self.fournisseur.id_service_fournisseur:
            payload["fournisseur"]["idServiceFournisseur"] = (
                self.fournisseur.id_service_fournisseur
            )
        if self.fournisseur.code_coordonnees_bancaires_fournisseur:
            payload["fournisseur"]["codeCoordonneesBancairesFournisseur"] = (
                self.fournisseur.code_coordonnees_bancaires_fournisseur
            )

        # --- Lignes de poste
        payload["lignePoste"] = []
        for lp in self.lignes_de_poste:
            payload["lignePoste"].append(
                {
                    "lignePosteNumero": lp.numero,
                    "lignePosteReference": lp.reference,
                    "lignePosteDenomination": lp.denomination,
                    "lignePosteQuantite": float(lp.quantite),
                    "lignePosteUnite": lp.unite,
                    "lignePosteMontantUnitaireHT": float(lp.montant_unitaire_ht),
                    "lignePosteMontantRemiseHT": float(lp.montant_remise_ht or 0),
                    "lignePosteTauxTvaManuel": float(lp.taux_tva_manuel or 0),
                }
            )

        # --- Lignes de TVA
        payload["ligneTva"] = []
        for lt in self.lignes_de_tva:
            payload["ligneTva"].append(
                {
                    "ligneTvaMontantBaseHtParTaux": float(lt.montant_base_ht),
                    "ligneTvaMontantTvaParTaux": float(lt.montant_tva),
                    "ligneTvaTauxManuel": float(lt.taux_manuel or 0),
                }
            )

        # --- Montants totaux
        payload["montantTotal"] = {
            "montantHtTotal": float(self.montant_total.montant_ht_total),
            "montantTVA": float(self.montant_total.montant_tva),
            "montantTtcTotal": float(self.montant_total.montant_ttc_total),
            "montantAPayer": float(self.montant_total.montant_a_payer),
        }

        if self.montant_total.montant_remise_globale_ttc is not None:
            payload["montantTotal"]["montantRemiseGlobaleTTC"] = float(
                self.montant_total.montant_remise_globale_ttc
            )
        if self.montant_total.motif_remise_globale_ttc:
            payload["montantTotal"]["motifRemiseGlobaleTTC"] = (
                self.montant_total.motif_remise_globale_ttc
            )

        # --- Ne surtout pas inclure la date_facture (provoque une 500)
        # (aucun champ "dateFacture" ajouté)

        # --- Nettoyage final : suppression des None
        return nettoyer_dict(payload)


# --- Modèle pour la génération Factur-X ---


class FactureFacturX(FactureBase):
    """Modèle de données pour une facture destinée à être convertie en Factur-X."""

    numero_facture: str
    date_echeance_paiement: str

    def get_facturx_type_code(self) -> str:
        """Détermine le code de type de document Factur-X (380 pour facture, 381 pour avoir)."""
        return "381" if self.references.type_facture == TypeFacture.AVOIR else "380"

    def get_facturx_mode_paiement_code(self) -> str:
        """Traduit le mode de paiement en code Factur-X standard."""
        match self.references.mode_paiement:
            case ModePaiement.CHEQUE:
                return "20"
            case ModePaiement.PRELEVEMENT:
                return "49"
            case ModePaiement.VIREMENT:
                return "30"
            case ModePaiement.ESPECE:
                return "10"
            case ModePaiement.AUTRE:
                return "57"
            case ModePaiement.REPORT:
                return "97"
            case _:
                # Cette branche ne devrait jamais être atteinte avec un Enum, mais c'est une bonne pratique.
                raise NotImplementedError(
                    f"Le mode de paiement '{self}' n'a pas de code Factur-X défini."
                )

    def generer_facturx(self, profil: ProfilFacturX) -> ConstructeurFacturX:
        """
        Point d'entrée pour le processus de construction d'un fichier Factur-X.
        Retourne un objet constructeur permettant de chaîner les opérations.
        """
        return ConstructeurFacturX(self, profil)
