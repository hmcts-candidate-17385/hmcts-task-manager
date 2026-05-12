from flask import jsonify
from marshmallow import ValidationError


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(err: ValidationError):
        return jsonify({"errors": err.messages}), 422
