import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import db
from .blueprints.mechanics import mechanics_bp
from .blueprints.customers import customers_bp
from .blueprints.inventory import inventory_bp
from .blueprints.service_ticket import service_ticket_bp

def create_app(config_name=None):
    # Compute project root so Flask can serve static/swagger.yaml
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(
        __name__,
        static_folder=os.path.join(project_root, 'static'),
        static_url_path='/static'
    )

    # Load config if provided (e.g. 'DevelopmentConfig' or 'TestingConfig')
    if config_name:
        app.config.from_object(f'config.{config_name}')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')

    # Set up Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL     = '/static/swagger.yaml'
    swaggerui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Service Center API Docs"}
    )
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    return app
