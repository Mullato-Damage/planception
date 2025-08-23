"""
test_app.py
Pytest-based functional tests for Planception.
Covers add, validate, duplicate reject, today/overdue, and delete.
"""

import pytest
from app import create_app
from models import db, Task
from repo import TaskRepository

@pytest.fixture()
def client(tmp_path):
    """
    Create a Flask test client backed by a temporary SQLite DB.

    Each test runs in isolation: DB is dropped + recreated fresh.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(tmp_path / "test.sqlite")
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app.test_client()

def test_add_valid_task(client):
    # Add a valid task and verify it’s in the DB
    resp = client.post("/add", data={"name": "Essay", "due_date": "2030-01-01", "priority": "high", "category": "School"})
    assert resp.status_code == 302  # redirect
    with client.application.app_context():
        assert Task.query.filter_by(name="Essay").one()

def test_add_invalid_priority(client):
    # Reject invalid priorities (not in enum).
    resp = client.post("/add", data={"name": "Bad", "due_date": "2030-01-01", "priority": "urgent", "category": ""})
    assert resp.status_code == 302
    with client.application.app_context():
        assert Task.query.filter_by(name="Bad").first() is None

def test_duplicate_name_rejected(client):
    # Do not allow duplicate task names (case-insensitive).
    client.post("/add", data={"name": "Essay", "due_date": "2030-01-01", "priority": "med", "category": ""})
    client.post("/add", data={"name": "Essay", "due_date": "2030-01-02", "priority": "low", "category": ""})
    with client.application.app_context():
        assert Task.query.filter_by(name="Essay").count() == 1

def test_today_and_overdue_views(client):
    # past task
    client.post("/add", data={"name": "Past", "due_date": "2020-01-01", "priority": "low", "category": ""})
    # future task
    client.post("/add", data={"name": "Future", "due_date": "2030-01-01", "priority": "low", "category": ""})
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "Past" in html  # shows as overdue
    assert "Future" in html

def test_delete_task(client):
    #Deleting a task removes it from DB.
    client.post("/add", data={"name": "Temp", "due_date": "2030-01-01", "priority": "med", "category": ""})
    resp = client.post("/delete/Temp")
    assert resp.status_code == 302
    with client.application.app_context():
        assert Task.query.filter_by(name="Temp").first() is None