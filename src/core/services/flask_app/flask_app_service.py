"""Service responsible only for Flask app creation and configuration."""

from flask import Flask
from flasgger import Swagger


class FlaskAppService:
    """Service responsible only for creating and configuring Flask application."""

    def create_flask_app(self) -> Flask:
        """
        Create and configure Flask application.

        Returns:
            Configured Flask application
        """
        app = Flask(__name__)

        # Setup Swagger for API documentation
        Swagger(app)

        return app
