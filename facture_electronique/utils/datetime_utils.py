from datetime import datetime


def format_datetime_to_iso(dt: datetime) -> str:
    # Format en ISO 8601 avec millisecondes et suffixe Z pour UTC
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}" + "Z"
