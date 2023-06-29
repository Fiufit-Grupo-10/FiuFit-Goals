import os

METRICS_SERVICE_URL = os.getenv("METRICS_SERVICE_URL", "")
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "")
DEFAULT_WEIGTH = 80
CATEGORY_MULTIPLIERS = {
    "Fuerza": 5,
    "Cardio": 7,
    "Yoga": 3,
    "Pilates": 4,
    "Baile": 4,
    "Meditacion": 1,
    "Hiit": 10,
    "Kickboxing": 10,
    "Tonificacion": 4,
    "Spinning": 4,
    "Cinta": 4,
    "Estirar": 2,
}
