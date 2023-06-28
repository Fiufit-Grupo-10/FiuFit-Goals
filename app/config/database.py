import os

MONGO_URL = os.getenv("MONGO_URL", "")
GOALS_COLLECTION_NAME = "goals"
TRAININGS_COLLECTION_NAME = "trainings"
DB_NAME = "goals_test"
METRICS_SERVICE_URL = os.getenv("METRICS_SERVICE_URL", "")
