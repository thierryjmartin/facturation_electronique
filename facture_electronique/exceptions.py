class ErreurConfiguration(Exception):
    """Exception levée lorsque la configuration de la bibliothèque est manquante ou invalide."""

    def __init__(self, nom_variable):
        self.nom_variable = nom_variable
        # Marquer la chaîne pour la traduction
        message = "La variable d'environnement \"{nom_variable}\" est requise mais n'a pas été trouvée.".format(
            nom_variable=nom_variable
        )
        super().__init__(message)


class FacturationAPIError(Exception):
    """Erreur générique pour les erreurs liées à l'API de facturation électronique."""

    pass


class FactureNonTrouveeError(FacturationAPIError):
    """Exception lorsque la facture n'est pas trouvée."""

    pass


class InvalidDataFacturxError(Exception):
    """Exception lorsqu'on l'objet Facture comprend des données qui sont incompatibles avec Facturx"""

    pass


class XSLTValidationError(Exception):
    """Erreur lorsque qu'on essaie de valider un facturx selon xslt et que ça ne passe pas"""

    pass
