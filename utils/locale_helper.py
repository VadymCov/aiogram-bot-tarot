LOCALE_MAP = {
    "ua": "C.UTF-8",
    "en": "C.UTF-8",
    "ru": "C.UTF-8",
}

def get_system_locale(lang: str) -> str:
    if not lang:
        lang = "ua"
    return LOCALE_MAP.get(lang, "C.UTF-8")