import pytest
import random

from api.dao.auth import AuthDAO
from api.exceptions.validation import ValidationException

from api.neo4j import get_driver

email = str(random.randint(1, 10000)) + "@neo4j.com"
password = "letmein"
name = "Random User"

@pytest.fixture(autouse=True)
def before_all(app):
    with app.app_context():
        driver = get_driver()

        def delete_user(tx):
            return tx.run("MATCH (u:User {email: $email}) DETACH DELETE u", email=email).consume()

        with driver.session() as session:
            session.execute_write(delete_user)
            session.close()


def test_unique_constraint(app):
    """
    If this error fails, try running the following query in your Sandbox to create the unique constraint
    CREATE CONSTRAINT UserEmailUnique ON ( user:User ) ASSERT (user.email) IS UNIQUE
    """

    def get_constraints(tx):
        return tx.run("""
            SHOW CONSTRAINTS
            YIELD name, labelsOrTypes, properties
            WHERE labelsOrTypes = ['User'] AND properties = ['email']
            RETURN *
        """).single()

    with app.app_context():
        with get_driver().session() as session:
            res = session.execute_read(get_constraints)

            assert res is not None

def test_validation_error(app):
    with app.app_context():
        driver = get_driver()

        dao = AuthDAO(driver, "secret")

        dao.register(email, password, name)

        with pytest.raises(ValidationException):
            dao.register(email, password, name)
