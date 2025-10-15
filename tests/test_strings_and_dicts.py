# -*- coding: utf-8 -*-

import pytest

# On importe les fonctions originales avec leurs noms anglais
# En supposant qu'elles se trouvent dans un module `strings_and_dicts`
from facture_electronique.utils.strings_and_dicts import (
    to_camel_case,
    transform_dict_keys,
)


class TestConversionCasseCamel:
    """
    Groupe de tests pour la fonction utilitaire `to_camel_case`.
    """

    @pytest.mark.parametrize(
        "texte_entree, resultat_attendu",
        [
            # Cas standards
            ("snake_case_exemple", "snakeCaseExemple"),
            ("kebab-case-exemple", "kebabCaseExemple"),
            ("un_mix-de-cas", "unMixDeCas"),
            # Cas limites
            ("motunique", "motunique"),
            ("dejaEnCamelCase", "dejaEnCamelCase"),
            ("", ""),
            # Cas avec séparateurs aux extrémités ou multiples
            ("_snake_case_avec_prefixe", "snakeCaseAvecPrefixe"),
            ("kebab-case-avec-suffixe-", "kebabCaseAvecSuffixe"),
            ("separateurs___multiples", "separateursMultiples"),
            ("un--seul--mot", "unSeulMot"),
        ],
    )
    def test_conversion_reussie(self, texte_entree, resultat_attendu):
        """Vérifie que la conversion en casse camel fonctionne pour divers cas."""
        assert to_camel_case(texte_entree) == resultat_attendu


class TestTransformationClesDictionnaire:
    """
    Groupe de tests pour la fonction récursive `transform_dict_keys`.
    """

    def test_dictionnaire_simple(self):
        """Vérifie la transformation sur un dictionnaire à un seul niveau."""
        dictionnaire_entree = {
            "premiere_cle": "valeur1",
            "deuxieme_key-avec-tiret": "valeur2",
        }
        resultat_attendu = {
            "premiereCle": "valeur1",
            "deuxiemeKeyAvecTiret": "valeur2",
        }
        resultat_obtenu = transform_dict_keys(dictionnaire_entree, to_camel_case)
        assert resultat_obtenu == resultat_attendu

    def test_dictionnaire_imbrique(self):
        """Vérifie la transformation sur un dictionnaire avec des niveaux imbriqués."""
        dictionnaire_entree = {
            "niveau_un": {"cle_imbriquee": "valeur_imbriquee", "autre-cle": 123},
            "cle_racine": "valeur_racine",
        }
        resultat_attendu = {
            "niveauUn": {"cleImbriquee": "valeur_imbriquee", "autreCle": 123},
            "cleRacine": "valeur_racine",
        }
        resultat_obtenu = transform_dict_keys(dictionnaire_entree, to_camel_case)
        assert resultat_obtenu == resultat_attendu

    def test_liste_de_dictionnaires(self):
        """Vérifie que la transformation s'applique aux dictionnaires dans une liste."""
        liste_entree = [
            {"premiere_entree": "a"},
            {"deuxieme_entree": {"cle_profonde": "b"}},
        ]
        resultat_attendu = [
            {"premiereEntree": "a"},
            {"deuxiemeEntree": {"cleProfonde": "b"}},
        ]
        resultat_obtenu = transform_dict_keys(liste_entree, to_camel_case)
        assert resultat_obtenu == resultat_attendu

    def test_structure_complexe(self):
        """Vérifie la transformation sur une structure mixte et complexe."""
        structure_entree = {
            "liste_de_donnees": [
                {"id_element": 1, "nom_element": "A"},
                {"id_element": 2, "details-supplementaires": {"etat_element": "actif"}},
            ],
            "meta_donnees": {"version_api": "v1.0"},
        }
        resultat_attendu = {
            "listeDeDonnees": [
                {"idElement": 1, "nomElement": "A"},
                {"idElement": 2, "detailsSupplementaires": {"etatElement": "actif"}},
            ],
            "metaDonnees": {"versionApi": "v1.0"},
        }
        resultat_obtenu = transform_dict_keys(structure_entree, to_camel_case)
        assert resultat_obtenu == resultat_attendu

    @pytest.mark.parametrize(
        "donnee_entree",
        [
            123,
            "une_chaine_simple",
            None,
            [],
            {},
        ],
    )
    def test_types_non_modifies(self, donnee_entree):
        """Vérifie que les types non-récursifs sont retournés inchangés."""
        assert transform_dict_keys(donnee_entree, to_camel_case) == donnee_entree
