import pytest

from app import create_app
from app.models import init_db


@pytest.fixture
def app(tmp_path):

    app = create_app()

    app.config["TESTING"] = True
    app.config["DATABASE_PATH"] = str(
        tmp_path / "test.db"
    )

    with app.app_context():
        init_db()

    yield app


@pytest.fixture
def client(app):

    return app.test_client()


def test_login_page(client):

    response = client.get("/login")

    assert response.status_code == 200


def test_register_page(client):

    response = client.get("/register")

    assert response.status_code == 200