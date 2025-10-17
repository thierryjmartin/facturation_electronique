from datetime import datetime, date


def obtenir_date_iso_maintenant() -> str:
    """
    Retourne la date et l'heure actuelles, au format ISO 8601
    Exemple: "2024-07-26"
    """
    return date.today().isoformat()


def format_datetime_to_iso(dt: datetime) -> str:
    # Format en ISO 8601 avec millisecondes et suffixe Z pour UTC
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}" + "Z"
