import logging

import uvicorn
from fastapi import FastAPI

from src.app.controller.transaction_controller import TransactionController
from src.app.repository.transaction_repository import TransactionRepository
from src.app.service.transaction_service import TransactionService
from src.app.utils.config.config import Config
from src.app.utils.database.db_connector import DatabaseConnector
from src.app.utils.middleware.middleware_registrar import MiddlewareRegistrar

app = FastAPI()
config = Config()

db_url = config.get("DATABASE_URL")
db_connector = DatabaseConnector(db_url)
transaction_repository = TransactionRepository(db_connector)
transaction_service = TransactionService(transaction_repository)
transaction_controller = TransactionController(transaction_service)

middleware_registrar = MiddlewareRegistrar(app)
middleware_registrar.register_cors_middleware()

app.include_router(transaction_controller.get_router())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
