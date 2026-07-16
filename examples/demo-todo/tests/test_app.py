import pytest

from app.main import app, reset_store


@pytest.fixture()
def client():
    reset_store()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_create_todo_defaults_priority_medium(client):
    res = client.post("/todos", json={"title": "no priority set"})
    assert res.status_code == 201
    assert res.get_json()["priority"] == "medium"


def test_create_todo_with_priority(client):
    res = client.post("/todos", json={"title": "Ship demo", "priority": "high"})
    assert res.status_code == 201
    body = res.get_json()
    assert body["title"] == "Ship demo"
    assert body["priority"] == "high"
    assert body["done"] is False


def test_create_todo_rejects_bad_priority(client):
    res = client.post("/todos", json={"title": "x", "priority": "urgent"})
    assert res.status_code == 400


def test_list_todos(client):
    client.post("/todos", json={"title": "a", "priority": "low"})
    res = client.get("/todos")
    assert res.status_code == 200
    assert len(res.get_json()["todos"]) == 1


def test_mark_done(client):
    created = client.post("/todos", json={"title": "a"}).get_json()
    res = client.patch(f"/todos/{created['id']}", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True
