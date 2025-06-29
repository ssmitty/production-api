"""Service responsible only for registering Flask routes."""

import logging
import pytz
from flask import Flask, request, jsonify, redirect, make_response

from src.config.settings import settings
from src.core.services.flask_app.flask_service_initializer_service import (
    FlaskServiceInitializerService,
)


class FlaskRouteRegistrationService:
    """Service responsible only for registering Flask routes."""

    def __init__(self, service_initializer: FlaskServiceInitializerService):
        """
        Initialize the route registration service.

        Args:
            service_initializer: Service containing initialized Flask services
        """
        self.services = service_initializer

    def register_routes(self, app: Flask) -> None:
        """
        Register all Flask application routes.

        Args:
            app: Flask application to register routes on
        """

        @app.route("/")
        def root():
            """Redirect to API documentation."""
            return redirect("/apidocs")

        @app.route("/", methods=["GET"])
        def home_form():
            """Home Page: Renders a simple HTML form for company name input."""
            return """
            <form method="post" action="/match">
                <input type="text" name="name" placeholder="Enter company name" required>
                <input type="submit" value="Match">
            </form>
            """

        @app.route("/match", methods=["POST"])
        def match_api():
            """
            Company Matcher API Endpoint
            ---
            consumes:
              - application/x-www-form-urlencoded
            parameters:
              - name: name
                in: formData
                type: string
                required: true
                description: The company name to match
            responses:
              200:
                description: JSON with match results
              400:
                description: Bad request (missing name)
              500:
                description: Internal server error
            """
            try:
                name = request.form.get("name")
                if not name:
                    return jsonify({"error": "No company name provided."}), 400

                # Perform matching using the service
                result = self.services.company_matcher.match_company(name)

                # Check if matching was successful
                if result.message == "No ticker data available":
                    logging.error("Ticker data is not available from the database.")
                    return (
                        jsonify(
                            {
                                "error": "Ticker data is currently unavailable. Please try again later."
                            }
                        ),
                        503,
                    )

                # Log API latency for monitoring
                logging.info(
                    "API Latency for '%s': %.4f seconds", name, result.api_latency
                )

                # Return structured response
                return jsonify(
                    {
                        "API_VERSION": settings.APP_VERSION,
                        "input_name": name,
                        "matched_name": result.matched_name,
                        "predicted_ticker": result.predicted_ticker,
                        "all_possible_tickers": result.all_possible_tickers,
                        "name_match_score": result.name_match_score,
                        "message": result.message,
                        "top_matches": result.top_matches,
                        "api_latency": result.api_latency,
                    }
                )

            except Exception as e:
                logging.error("API error in /match: %s", e)
                return jsonify({"error": "Internal server error"}), 500

        @app.route("/update_tickers", methods=["GET"])
        def update_tickers():
            """
            Update Tickers Dataset by fetching from Alpha Vantage API
            ---
            responses:
              200:
                description: Tickers updated successfully or error message
            """
            try:
                # Fetch ticker data using the service
                tickers_df = self.services.ticker_updater.fetch_ticker_dataframe()

                # Save using the dataframe saver micro-service
                self.services.dataframe_saver.save_tickers_dataframe(tickers_df)

                message = "Tickers updated successfully."

            except Exception as err:
                logging.error("Error updating tickers: %s", err)
                message = f"Error updating tickers: {err}"

            html = f"""
                <html>
                    <div class='result'>{message}</div>
                </html>
            """
            response = make_response(html)
            response.headers["X-API-Version"] = settings.APP_VERSION
            return response

        @app.route("/latest_tickers", methods=["GET"])
        def latest_tickers():
            """
            Get the last update time of the tickers dataset, optionally in a specific timezone.
            ---
            parameters:
              - name: tz
                in: query
                type: string
                required: false
                description: The timezone to display the time in (e.g., 'America/New_York'). Defaults to UTC.
                default: UTC
            responses:
              200:
                description: Last update time of tickers in the specified or default timezone.
              400:
                description: Invalid timezone provided.
              500:
                description: Error getting ticker update time.
            """
            # Get timezone from query param, default to UTC
            tz_name = request.args.get("tz", "UTC")

            # Use metadata service to get last update time
            result = self.services.metadata_service.get_last_update_time(tz_name)

            if result["status"] != 200:
                return jsonify({"error": result["error"]}), result["status"]

            return (
                jsonify(
                    {
                        "API_VERSION": settings.APP_VERSION,
                        "last_updated": result["last_updated"],
                        "timezone": result["timezone"],
                    }
                ),
                200,
            )

        @app.route("/timezones", methods=["GET"])
        def list_timezones():
            """
            Get a list of all available timezones.
            ---
            responses:
              200:
                description: A JSON list of available timezone strings.
            """
            return jsonify(list(pytz.all_timezones))

        @app.route("/health", methods=["GET"])
        def health_check():
            """
            Health check endpoint to verify service status.
            ---
            responses:
              200:
                description: Service is healthy
              503:
                description: Service is unhealthy
            """
            try:
                # Check database health using micro-service
                is_healthy = self.services.health_service.check_health()

                if is_healthy:
                    return (
                        jsonify(
                            {
                                "API_VERSION": settings.APP_VERSION,
                                "status": "healthy",
                                "database": "connected",
                            }
                        ),
                        200,
                    )
                else:
                    return (
                        jsonify(
                            {
                                "API_VERSION": settings.APP_VERSION,
                                "status": "unhealthy",
                                "database": "disconnected",
                            }
                        ),
                        503,
                    )

            except Exception as e:
                logging.error("Health check error: %s", e)
                return (
                    jsonify(
                        {
                            "API_VERSION": settings.APP_VERSION,
                            "status": "unhealthy",
                            "error": str(e),
                        }
                    ),
                    503,
                )
