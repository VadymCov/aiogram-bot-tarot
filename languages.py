TEXTS = {
    "welcome": {
        "ru": "🌟 Добро пожаловать в астрологического бота!",
        "ua": "🌟 Ласкаво просимо до астрологічного бота!",
        "en": "🌟 Welcome to the astrology bot!"
    },

    "chose_language": {
        "ru": "Выберите язык:",
        "ua": "Оберіть мову:",
        "en": "Choose your language:"
    },

    "language_set": {
        "ru": "Язык установлен!",
        "ua": "Мову встановлено!",
        "en": "Language set!"
    }

}

def get_text(key, lang="ru"):
    return TEXTS.get(key, {}).get(lang, TEXTS[key]["ru"])