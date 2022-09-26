import os
from neo4j.exceptions import Neo4jError

import pytest

from api.dao.auth import AuthDAO
from api.neo4j import get_driver

email = "graphacademy@neo4j.com"
password = "letmein"
name = "Graph Academy"

@pytest.fixture(autouse=True)
def before_all(app):
    with app.app_context():
        driver = get_driver()

        def delete_user(tx):
            return tx.run("MATCH (u:User {email: $email}) DETACH DELETE u", email=email).consume()

        with driver.session() as session:
            session.execute_write(delete_user)
            session.close()

def test_register_user(app):
    with app.app_context():
        driver = get_driver()

        dao = AuthDAO(driver, os.environ.get('JWT_SECRET'))

        user = dao.register(email, password, name)

        assert user["userId"] is not None
        assert user["name"] == name
        assert "password" not in user
        assert user["userId"] is not None
        assert user["token"] is not None
