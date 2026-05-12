import os

from flask import Flask, jsonify, render_template_string

from app.extensions import db
from flask_cors import CORS

from app.errors import register_error_handlers
from app.openapi import build_openapi_spec

_SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Task API — Swagger UI</title>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => {
      window.ui = SwaggerUIBundle({
        url: "{{ openapi_url }}",
        dom_id: "#swagger-ui",
      });
    };
  </script>
</body>
</html>
"""


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", "sqlite:///tasks.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    register_error_handlers(app)

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "hmcts-task-manager API",
                "tasks": "/api/tasks",
                "openapi": "/openapi.json",
                "docs": "/docs",
            }
        )

    @app.get("/openapi.json")
    def openapi_json():
        return jsonify(build_openapi_spec())

    @app.get("/docs")
    def swagger_docs():
        return render_template_string(
            _SWAGGER_UI_HTML, openapi_url="/openapi.json"
        )

    from .routes import tasks_bp

    app.register_blueprint(tasks_bp)

    from . import models  # noqa: F401 — register Task metadata

    with app.app_context():
        db.create_all()

    return app
