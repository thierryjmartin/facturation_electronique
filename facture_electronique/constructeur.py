from __future__ import annotations
import typing
import os
import shutil
import tempfile
from pathlib import Path
import logging

import facturx
from .utils.facturx import (
    _GenerateurXML,
    ProfilFacturX,
    valider_xml_facturx_schematron,
    gen_xml_depuis_facture,
)
from .utils.pdfs import convert_to_pdfa, sign_pdf

if typing.TYPE_CHECKING:
    from .models import FactureFacturX

logger = logging.getLogger(__name__)


class ConstructeurFacturX:
    """
    Implémente une interface fluide pour construire un PDF Factur-X.
    Ne pas instancier directement. Utiliser `FactureFacturX.generer_facturx()`.
    """

    def __init__(self, facture: FactureFacturX, profil: ProfilFacturX):
        self.facture = facture
        self.profil = profil
        self.xml_str: str = None
        self.chemin_pdf_courant: Path = None
        self.est_valide: bool = False
        self._fichiers_temporaires = []

        generateur = _GenerateurXML(self.facture)
        objet_xml = generateur.generer_objet_xml(self.profil)
        self.xml_str = gen_xml_depuis_facture(objet_xml)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._nettoyer_temporaires()

    def _creer_fichier_temporaire(self, suffix: str) -> Path:
        fd, chemin = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        chemin_path = Path(chemin)
        self._fichiers_temporaires.append(chemin_path)
        return chemin_path

    def _nettoyer_temporaires(self):
        for chemin in self._fichiers_temporaires:
            try:
                chemin.unlink(missing_ok=True)
            except OSError:
                pass

    def valider_conformite(self):
        """Valide le XML interne contre le Schematron du profil. Requis avant intégration."""
        if not self.xml_str:
            raise RuntimeError("Le XML n'a pas été généré, impossible de valider.")

        valider_xml_facturx_schematron(self.xml_str, self.profil)
        self.est_valide = True
        return self

    def integrer_dans_pdfa(self, chemin_pdf_source: str):
        """Convertit un PDF source en PDF/A-3 et y attache le XML Factur-X."""
        if not self.est_valide:
            raise RuntimeError(
                "La conformité doit être validée avec `.valider_conformite()` avant l'intégration au PDF."
            )

        chemin_pdfa = self._creer_fichier_temporaire(suffix=".pdfa.pdf")
        chemin_facturx = self._creer_fichier_temporaire(suffix=f".{self.profil.id_str}.pdf")
        convert_to_pdfa(chemin_pdf_source, chemin_pdfa)

        facturx.generate_from_file(
            chemin_pdfa,
            self.xml_str,
            output_pdf_file=str(chemin_facturx),
            flavor="factur-x",
            level=self.profil.name.lower(),
            check_xsd=True,
        )

        self.chemin_pdf_courant = chemin_facturx
        return self

    def signer_pdf(self, cle: str, certificat: str, autres_certs: tuple = tuple()):
        """Signe numériquement le PDF en cours de construction."""
        if not self.chemin_pdf_courant:
            raise RuntimeError(
                "Un PDF doit être généré (via `integrer_dans_pdfa`) avant de pouvoir être signé."
            )

        chemin_sortie = self._creer_fichier_temporaire(suffix=".signed.pdf")
        sign_pdf(
            str(self.chemin_pdf_courant),
            str(chemin_sortie),
            cle,
            certificat,
            autres_certs,
        )

        logger.warning("AVERTISSEMENT : La signature numérique peut invalider la conformité PDF/A.")
        self.chemin_pdf_courant = chemin_sortie
        return self

    def enregistrer_sous(self, chemin_final: str) -> dict:
        """Sauvegarde le PDF final et nettoie les fichiers temporaires."""
        if not self.chemin_pdf_courant:
            raise RuntimeError("Aucun PDF n'a été généré à enregistrer.")

        destination = Path(chemin_final)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(self.chemin_pdf_courant, destination)

        if self.chemin_pdf_courant in self._fichiers_temporaires:
            self._fichiers_temporaires.remove(self.chemin_pdf_courant)

        self._nettoyer_temporaires()

        return {"chemin_fichier": str(destination), "profil": self.profil.name}
