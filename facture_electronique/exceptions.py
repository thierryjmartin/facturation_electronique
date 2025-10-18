import gettext

_ = gettext.gettext


class ErreurConfiguration(Exception):
    """Levée lorsqu'une variable de configuration requise est manquante."""

    def __init__(self, nom_variable):
        self.nom_variable = nom_variable
        # Marquer la chaîne pour la traduction
        message = "La variable d'environnement \"{nom_variable}\" est requise mais n'a pas été trouvée.".format(
            nom_variable=nom_variable
        )
        super().__init__(message)


class FacturationAPIError(Exception):
    """Classe de base pour les erreurs retournées par une API externe."""

    pass


class FactureNonTrouveeError(FacturationAPIError):
    """Levée spécifiquement lorsqu'une facture n'est pas trouvée via l'API."""

    pass


class InvalidDataFacturxError(Exception):
    """Levée lorsque les données d'une facture sont incompatibles avec un profil Factur-X."""

    pass


class XSLTValidationError(Exception):
    """Levée lorsque la validation d'un XML Factur-X contre son fichier XSLT échoue."""

    def __init__(self, messages: list, *args):
        self.messages = messages
        # Translators: The placeholder is the number of validation errors.
        message = _("{num_errors} erreur(s) de validation XSLT.").format(num_errors=len(messages))
        super().__init__(message, *args)

    def __str__(self):
        # Fournir une représentation simple et lisible
        # Translators: The placeholder is a list of the first 3 error messages.
        details = "\n - ".join(self.messages[:3])
        return f"{super().__str__()} " + _("Détails :\n - {details}").format(details=details)
