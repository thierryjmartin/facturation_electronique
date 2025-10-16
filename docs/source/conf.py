# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Facturation Électronique"
copyright = "2025, Thierry"
author = "Thierry"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "fr"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for doctest -----------------------------------------------------
doctest_global_setup = """
import os
from decimal import Decimal
from facture_electronique.api.chorus_pro import ChorusProAPI
from facture_electronique.models import (
    FactureChorus, FactureFacturX, ModeDepot, Destinataire, Fournisseur,
    CadreDeFacturation, CodeCadreFacturation, References, TypeFacture,
    TypeTVA, ModePaiement, LigneDePoste, LigneDeTVA, MontantTotal,
    AdressePostale, CategorieTVA, PieceJointePrincipale
)
from facture_electronique.utils.files import get_absolute_path, file_to_base64, guess_mime_type, get_file_extension
from facture_electronique.utils.pdfs import convert_to_pdfa, sign_pdf
from facture_electronique.utils.facturx import (
    gen_xml_depuis_facture,
    valider_xml_facturx_schematron,
    FACTURX_EN16931,
)
import facturx

os.environ['PISTE_CLIENT_ID'] = 'dummy'
os.environ['PISTE_CLIENT_SECRET'] = 'dummy'
os.environ['PISTE_SANDBOX_CLIENT_ID'] = 'dummy'
os.environ['PISTE_SANDBOX_CLIENT_SECRET'] = 'dummy'
os.environ['CHORUS_PRO_LOGIN'] = 'dummy'
os.environ['CHORUS_PRO_PASSWORD'] = 'dummy'
"""
