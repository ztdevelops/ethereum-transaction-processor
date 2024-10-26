import unittest
from unittest.mock import MagicMock

from fastapi import FastAPI

from src.app.utils.middleware.middleware_registrar import MiddlewareRegistrar


class TestMiddlewareRegistrar(unittest.TestCase):
    def setUp(self):
        self.app = MagicMock(spec=FastAPI)
        self.middleware_registrar = MiddlewareRegistrar(self.app)

    def test_register_cors_middleware(self):
        from fastapi.middleware.cors import CORSMiddleware

        # Act
        self.middleware_registrar.register_cors_middleware()

        # Assert
        self.app.add_middleware.assert_called_once()
        self.app.add_middleware.assert_called_with(
            CORSMiddleware,
            allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )