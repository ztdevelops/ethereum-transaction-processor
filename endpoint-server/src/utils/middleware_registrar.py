from fastapi import FastAPI

from utils.config import Config

config = Config()


class MiddlewareRegistrar:
    """
    Class for registering middleware to a FastAPI application.

    Attributes:
        __app (FastAPI): The FastAPI application instance.
    """

    def __init__(self, app: FastAPI):
        """
        Initialize the MiddlewareRegistrar with a FastAPI application instance.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        self.__app = app

    def register_cors_middleware(self):
        """
        Register the CORS middleware to the FastAPI application.
        """
        from fastapi.middleware.cors import CORSMiddleware
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
