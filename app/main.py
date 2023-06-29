from fastapi import FastAPI
from app.api.goals import routes as goals_routes
from app.api.trainings_info import routes as training_routes
from app.config.database import DB_NAME, MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient
from ddtrace.contrib.asgi import TraceMiddleware
from ddtrace import config
import asyncio
from app.config.config import DEV_ENV, logger

config.fastapi["service_name"] = "goals-service"

app = FastAPI()

if DEV_ENV == "true":
    app.add_middleware(TraceMiddleware)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb_client.get_io_loop = asyncio.get_event_loop
    app.mongodb = app.mongodb_client[DB_NAME]
    logger.info("Succesfully connected to database")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(goals_routes.router)
app.include_router(training_routes.router)
