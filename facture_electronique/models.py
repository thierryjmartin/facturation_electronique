from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from decimal import Decimal
from typing import List, Optional, Annotated

from .utils.strings_and_dicts import to_camel_case


FRENCH_CAMEL_CASE_CONFIG = ConfigDict(
    alias_generator=to_camel_case,
    populate_by_name=True,
)


class CodeCadreFacturation(str, Enum):
    A1_FACTURE_FOURNISSEUR = "A1_FACTURE_FOURNISSEUR"
    A2_FACTURE_FOURNISSEUR_DEJA_PAYEE = "A2_FACTURE_FOURNISSEUR_DEJA_PAYEE"
    A9_FACTURE_SOUSTRAITANT = "A9_FACTURE_SOUSTRAITANT"
    A12_FACTURE_COTRAITANT = "A12_FACTURE_COTRAITANT"


class CadreDeFacturation(BaseModel):
    model_config = FRENCH_CAMEL_CASE_CONFIG
    code_cadre_facturation: CodeCadreFacturation
    code_service_valideur: Optional[str] = None
    code_structure_valideur: Optional[str] = None


class AdressePostale(BaseModel):
    model_config = FRENCH_CAMEL_CASE_CONFIG
    code_postal: Optional[str] = None
    ligne_un: Optional[str] = None
    ligne_deux: Optional[str] = None
    nom_ville: Optional[str] = None
    pays_code_iso: Optional[str] = "FR"


class Destinataire(BaseModel):
    model_config = FRENCH_CAMEL_CASE_CONFIG
    code_destinataire: str  # SIRET
    code_service_executant: Optional[str] = None
    nom: Optional[str] = None
    adresse_postale: Optional[AdressePostale] = None


class Fournisseur(BaseModel):
    model_config = FRENCH_CAMEL_CASE_CONFIG
    id_fournisseur: int  # Identifiant Chorus Pro
    code_coordonnees_bancaires_fournisseur: Optional[int] = None
    id_service_fournisseur: Optional[int] = None
    nom: Optional[str] = None
    siret: Optional[str] = None
    numero_tva_intra: Optional[str] = None
    adresse_postale: Optional[AdressePostale] = None


class CategorieTVA(str, Enum):
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
    REMISE_PUBLICITAIRE = "AA"
    SUPPLEMENT_EMBALLAGE = "ABL"
    AUTRES_SERVICES = "ADR"
    ENLEVEMENT = "ADT"
    COUTS_TRANSPORT = "FC"
    FRAIS_FINANCIERS = "FI"
    ETIQUETAGE = "LA"


class LigneDePoste(BaseModel):
    model_config = FRENCH_CAMEL_CASE_CONFIG
    numero: int
    reference: Optional[str] = None
    denomination: str
    quantite: float
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
    taux_tva_manuel: Optional[float] = None
    categorie_tva: Optional[CategorieTVA] = None
    date_debut_periode: Optional[str] = None
    date_fin_periode: Optional[str] = None
    code_raison_reduction: Optional[CodeRaisonReduction] = None
    raison_reduction: Optional[str] = None


class LigneDeTVA(BaseModel):
    model_config = FRENCH_CAMEL_CASE_CONFIG
    montant_base_ht: Annotated[
        Decimal,
        Field(
            ge=0,
            max_digits=12,
            decimal_places=4,
            description="Montant de base HT pour cette ligne de TVA.",
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
    taux_manuel: Optional[float] = None
    categorie: Optional[CategorieTVA] = None


class MontantTotal(BaseModel):
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
    model_config = FRENCH_CAMEL_CASE_CONFIG
    designation: str
    id: int
    id_liaison: int
    numero_ligne_facture: int
    type: str


class PieceJointePrincipale(BaseModel):
    model_config = FRENCH_CAMEL_CASE_CONFIG
    designation: str
    id: Optional[int] = None


class ModePaiement(str, Enum):
    CHEQUE = "CHEQUE"
    PRELEVEMENT = "PRELEVEMENT"
    VIREMENT = "VIREMENT"
    ESPECE = "ESPECE"
    AUTRE = "AUTRE"
    REPORT = "REPORT"


class TypeFacture(str, Enum):
    FACTURE = "FACTURE"
    AVOIR = "AVOIR"


class TypeTVA(str, Enum):
    SUR_DEBIT = "TVA_SUR_DEBIT"
    SUR_ENCAISSEMENT = "TVA_SUR_ENCAISSEMENT"
    EXONERATION = "EXONERATION"
    SANS_TVA = "SANS_TVA"


class References(BaseModel):
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
    SAISIE_API = "SAISIE_API"
    DEPOT_PDF_API = "DEPOT_PDF_API"
    DEPOT_PDF_SIGNE_API = "DEPOT_PDF_SIGNE_API"


# --- Modèles de base ---


class FactureBase(BaseModel):
    model_config = FRENCH_CAMEL_CASE_CONFIG
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
    numero_facture_saisi: Optional[str] = None
    date_facture: Optional[str] = None
    pieces_jointes_principales: Optional[List[PieceJointePrincipale]] = None

    def to_api_payload(self) -> dict:
        """Génère le payload JSON pour l'API Chorus Pro."""
        # Pydantic s'occupe de la conversion en camelCase grâce à la config
        return self.model_dump(by_alias=True, exclude_unset=True)


# --- Modèle pour la génération Factur-X ---


class FactureFacturX(FactureBase):
    numero_facture: str
    date_facture: str
    date_echeance_paiement: str

    def to_facturx_minimum(self):
        from .utils.facturx import gen_facturx_minimum

        return gen_facturx_minimum(self)

    def to_facturx_basic(self):
        from .utils.facturx import gen_facturx_basic

        return gen_facturx_basic(self)

    def to_facturx_en16931(self):
        from .utils.facturx import gen_facturx_en16931

        return gen_facturx_en16931(self)
