from marshmallow import Schema, fields, validate

ALLOWED_STATUSES = ("pending", "in_progress", "completed", "cancelled")


class TaskCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    description = fields.Str(required=False, allow_none=True, load_default=None)
    status = fields.Str(
        required=True,
        validate=validate.OneOf(ALLOWED_STATUSES),
    )
    due_date = fields.DateTime(required=True, metadata={"format": "date-time"})


class TaskStatusUpdateSchema(Schema):
    status = fields.Str(
        required=True,
        validate=validate.OneOf(ALLOWED_STATUSES),
    )
