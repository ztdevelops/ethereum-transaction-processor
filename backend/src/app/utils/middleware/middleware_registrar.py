from fastapi import FastAPI

from src.app.utils.config import Config

config = Config()


class MiddlewareRegistrar:
    """
    Class for registering middleware to a FastAPI application.

    Attributes:
        app (FastAPI): The FastAPI application instance.
    """

    def __init__(self, app: FastAPI):
        """
        Initializes the MiddlewareRegistrar with the given FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        self.app = app

    def register_cors_middleware(self):
        """
        Registers the CORS middleware to the FastAPI application.
        """
        from fastapi.middleware.cors import CORSMiddleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
