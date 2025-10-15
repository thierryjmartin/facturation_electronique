# -*- coding: utf-8 -*-

"""
Module principal pour la bibliothèque de facturation électronique.

Ce module expose les classes et fonctions les plus importantes de la bibliothèque
pour une utilisation simplifiée.
"""

from .api.chorus_pro import ChorusProAPI
from .api.pannylane import PennylaneAPI
from .api.sage import SAGEAPI
from .models import (
    AdressePostale,
    CadreDeFacturation,
    CategorieTVA,
    CodeCadreFacturation,
    CodeRaisonReduction,
    Destinataire,
    FactureBase,
    FactureChorus,
    FactureFacturX,
    Fournisseur,
    LigneDePoste,
    LigneDeTVA,
    ModeDepot,
    ModePaiement,
    MontantTotal,
    PieceJointeComplementaire,
    PieceJointePrincipale,
    References,
    TypeFacture,
    TypeTVA,
)
from .utils.facturx import (
    FACTURX_BASIC,
    FACTURX_EN16931,
    FACTURX_MINIMUM,
    gen_facturx_basic,
    gen_facturx_en16931,
    gen_facturx_minimum,
    gen_xml_depuis_facture,
    valider_xml_xldt,
)
from .utils.files import (
    file_to_base64,
    get_absolute_path,
    get_file_extension,
    guess_mime_type,
)
from .utils.pdfs import convert_to_pdfa, sign_pdf

__all__ = [
    # API Clients
    "ChorusProAPI",
    "PennylaneAPI",
    "SAGEAPI",
    # Models
    "CodeCadreFacturation",
    "CadreDeFacturation",
    "AdressePostale",
    "Destinataire",
    "Fournisseur",
    "CategorieTVA",
    "CodeRaisonReduction",
    "LigneDePoste",
    "LigneDeTVA",
    "MontantTotal",
    "PieceJointeComplementaire",
    "PieceJointePrincipale",
    "ModePaiement",
    "TypeFacture",
    "TypeTVA",
    "References",
    "ModeDepot",
    "FactureBase",
    "FactureChorus",
    "FactureFacturX",
    # Factur-X utils
    "gen_facturx_minimum",
    "gen_facturx_basic",
    "gen_facturx_en16931",
    "gen_xml_depuis_facture",
    "valider_xml_xldt",
    "FACTURX_MINIMUM",
    "FACTURX_BASIC",
    "FACTURX_EN16931",
    # File utils
    "file_to_base64",
    "guess_mime_type",
    "get_file_extension",
    "get_absolute_path",
    # PDF utils
    "convert_to_pdfa",
    "sign_pdf",
]
