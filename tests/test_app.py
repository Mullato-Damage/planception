import pytest
from app import create_app
from models import db, Task
from repo import TaskRepository

@pytest.fixture()
def client(tmp_path):
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
    resp = client.post("/add", data={"name": "Essay", "due_date": "2030-01-01", "priority": "high", "category": "School"})
    assert resp.status_code == 302  # redirect
    with client.application.app_context():
        assert Task.query.filter_by(name="Essay").one()

def test_add_invalid_priority(client):
    resp = client.post("/add", data={"name": "Bad", "due_date": "2030-01-01", "priority": "urgent", "category": ""})
    assert resp.status_code == 302
    with client.application.app_context():
        assert Task.query.filter_by(name="Bad").first() is None

def test_duplicate_name_rejected(client):
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
    client.post("/add", data={"name": "Temp", "due_date": "2030-01-01", "priority": "med", "category": ""})
    resp = client.post("/delete/Temp")
    assert resp.status_code == 302
    with client.application.app_context():
        assert Task.query.filter_by(name="Temp").first() is None