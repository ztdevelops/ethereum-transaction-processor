import logging

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from controller.transactions_controller import TransactionsController
from repository.transactions_repository import TransactionsRepository
from service.transactions_service import TransactionsService
from utils.config import Config
from utils.middleware_registrar import MiddlewareRegistrar
from utils.mongodb_connector import MongoDBConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
config = Config()

# Initialising Transactions components
db_connector = MongoDBConnector(config.get("MONGODB_URL"))
transactions_repository = TransactionsRepository(db_connector)
transactions_service = TransactionsService(transactions_repository)
transactions_controller = TransactionsController(transactions_service)

# Registering for CORS
middleware_registrar = MiddlewareRegistrar(app)
middleware_registrar.register_cors_middleware()

# Including routes defined in Transactions controller
app.include_router(transactions_controller.get_router())


# Setting up route to access Swagger UI
@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
