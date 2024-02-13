from fastapi_jwt_auth import AuthJWT
from fastapi.testclient import TestClient
from main import app
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from models.models import Base

from .db_fixtures import users, permission_groups, ecgs, leads, lead_analysis


@pytest.fixture(scope="session", autouse=True)
def db_session():
    test_sqlalchemy_database_url = os.environ["DATABASE_URI"]
    engine = create_engine(test_sqlalchemy_database_url)

    if database_exists(test_sqlalchemy_database_url):
        drop_database(test_sqlalchemy_database_url)

    create_database(test_sqlalchemy_database_url)

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db_session = SessionLocal()

    for group in permission_groups:
        db_session.add(group)
    for user in users:
        db_session.add(user)
    for ecg in ecgs:
        db_session.add(ecg)
    for lead in leads:
        db_session.add(lead)
    for la in lead_analysis:
        db_session.add(la)

    db_session.commit()

    yield db_session

    db_session.close()

    drop_database(test_sqlalchemy_database_url)
    engine.dispose()


@pytest.fixture(scope="module")
def base_client():
    return TestClient(app)


def generate_authenticated_client(client, user_id: int, permissions: list = None):
    auth = AuthJWT()
    access_token = auth.create_access_token(
        subject=str(user_id), user_claims={"permissions": list(permissions)}
    )
    # Clone the client to not interfere with other tests
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client


@pytest.fixture(scope="module")
def authenticated_user_admin_client(base_client):
    permissions = ["user:create", "user:read", "user:update", "user:delete"]
    client = generate_authenticated_client(
        base_client, user_id=users[0].id, permissions=permissions
    )
    yield client


@pytest.fixture(scope="module")
def authenticated_ecg_operator_client(base_client):
    permissions = ["ecg:create", "ecg:read"]
    client = generate_authenticated_client(
        base_client, user_id=users[1].id, permissions=permissions
    )
    yield client
