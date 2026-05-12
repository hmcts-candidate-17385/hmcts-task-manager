import json


def _task_json(**overrides):
    body = {
        "title": "Review bundle",
        "description": "Urgent",
        "status": "pending",
        "due_date": "2030-03-15T10:00:00+00:00",
    }
    body.update(overrides)
    return body


def test_list_empty_then_create_and_list(client):
    r = client.get("/api/tasks")
    assert r.status_code == 200
    assert r.get_json() == []

    r = client.post(
        "/api/tasks",
        data=json.dumps(_task_json()),
        content_type="application/json",
    )
    assert r.status_code == 201
    created = r.get_json()
    assert created["id"] == 1
    assert created["title"] == "Review bundle"
    assert created["status"] == "pending"

    r2 = client.get("/api/tasks")
    assert r2.status_code == 200
    assert len(r2.get_json()) == 1


def test_create_without_description(client):
    body = _task_json()
    del body["description"]
    r = client.post(
        "/api/tasks",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert r.status_code == 201
    assert r.get_json()["description"] is None


def test_get_by_id(client):
    client.post(
        "/api/tasks",
        data=json.dumps(_task_json(title="One")),
        content_type="application/json",
    )
    r = client.get("/api/tasks/1")
    assert r.status_code == 200
    assert r.get_json()["title"] == "One"


def test_get_by_id_not_found(client):
    r = client.get("/api/tasks/999")
    assert r.status_code == 404
    assert r.get_json()["message"] == "Task not found"


def test_patch_status(client):
    client.post(
        "/api/tasks",
        data=json.dumps(_task_json(status="pending")),
        content_type="application/json",
    )
    r = client.patch(
        "/api/tasks/1",
        data=json.dumps({"status": "in_progress"}),
        content_type="application/json",
    )
    assert r.status_code == 200
    assert r.get_json()["status"] == "in_progress"


def test_patch_status_not_found(client):
    r = client.patch(
        "/api/tasks/99",
        data=json.dumps({"status": "completed"}),
        content_type="application/json",
    )
    assert r.status_code == 404


def test_patch_invalid_status(client):
    client.post(
        "/api/tasks",
        data=json.dumps(_task_json()),
        content_type="application/json",
    )
    r = client.patch(
        "/api/tasks/1",
        data=json.dumps({"status": "invalid"}),
        content_type="application/json",
    )
    assert r.status_code == 422


def test_delete_task(client):
    client.post(
        "/api/tasks",
        data=json.dumps(_task_json()),
        content_type="application/json",
    )
    r = client.delete("/api/tasks/1")
    assert r.status_code == 204
    assert r.get_data(as_text=True) == ""
    assert client.get("/api/tasks/1").status_code == 404


def test_create_validation_empty_title(client):
    r = client.post(
        "/api/tasks",
        data=json.dumps(
            {
                "title": "",
                "status": "pending",
                "due_date": "2030-01-01T00:00:00+00:00",
            }
        ),
        content_type="application/json",
    )
    assert r.status_code == 422


def test_post_requires_json(client):
    r = client.post("/api/tasks", data="not-json", content_type="text/plain")
    assert r.status_code == 415


def test_openapi_json(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.get_json()
    assert spec["openapi"] == "3.0.3"
    assert "/api/tasks" in spec["paths"]
