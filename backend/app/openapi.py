"""OpenAPI 3 document for /openapi.json (kept in sync with routes)."""


def build_openapi_spec() -> dict:
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Caseworker Task API",
            "version": "1.0.0",
            "description": "HMCTS-style task API for caseworkers.",
        },
        "servers": [{"url": "/", "description": "Current host"}],
        "paths": {
            "/api/tasks": {
                "get": {
                    "summary": "List all tasks",
                    "operationId": "listTasks",
                    "responses": {
                        "200": {
                            "description": "Array of tasks",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Task"},
                                    }
                                }
                            },
                        }
                    },
                },
                "post": {
                    "summary": "Create a task",
                    "operationId": "createTask",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TaskCreate"}
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Task"}
                                }
                            },
                        },
                        "422": {"$ref": "#/components/responses/ValidationError"},
                    },
                },
            },
            "/api/tasks/{task_id}": {
                "parameters": [
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                    }
                ],
                "get": {
                    "summary": "Get task by ID",
                    "operationId": "getTask",
                    "responses": {
                        "200": {
                            "description": "Task",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Task"}
                                }
                            },
                        },
                        "404": {"$ref": "#/components/responses/NotFound"},
                    },
                },
                "patch": {
                    "summary": "Update task status",
                    "operationId": "patchTaskStatus",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TaskStatusUpdate"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Updated task",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Task"}
                                }
                            },
                        },
                        "404": {"$ref": "#/components/responses/NotFound"},
                        "422": {"$ref": "#/components/responses/ValidationError"},
                    },
                },
                "delete": {
                    "summary": "Delete a task",
                    "operationId": "deleteTask",
                    "responses": {
                        "204": {"description": "Deleted"},
                        "404": {"$ref": "#/components/responses/NotFound"},
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "Task": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "description": {"type": "string", "nullable": True},
                        "status": {
                            "type": "string",
                            "enum": list(
                                ("pending", "in_progress", "completed", "cancelled")
                            ),
                        },
                        "due_date": {"type": "string", "format": "date-time"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                },
                "TaskCreate": {
                    "type": "object",
                    "required": ["title", "status", "due_date"],
                    "properties": {
                        "title": {"type": "string", "maxLength": 120},
                        "description": {"type": "string", "nullable": True},
                        "status": {
                            "type": "string",
                            "enum": list(
                                ("pending", "in_progress", "completed", "cancelled")
                            ),
                        },
                        "due_date": {"type": "string", "format": "date-time"},
                    },
                },
                "TaskStatusUpdate": {
                    "type": "object",
                    "required": ["status"],
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": list(
                                ("pending", "in_progress", "completed", "cancelled")
                            ),
                        }
                    },
                },
            },
            "responses": {
                "NotFound": {
                    "description": "Not found",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {"message": {"type": "string"}},
                            }
                        }
                    },
                },
                "ValidationError": {
                    "description": "Validation failed",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "errors": {"type": "object"},
                                },
                            }
                        }
                    },
                },
            },
        },
    }
