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
