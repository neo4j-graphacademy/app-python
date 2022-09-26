import pytest

from api.dao.auth import AuthDAO
from api.neo4j import get_driver

email = 'authenticated@neo4j.com'
password = 'AuthenticateM3!'
name = 'Authenticated User'

# TODO: Run this test before all
# @pytest.fixture()
# def before_all(app):
#     with app.app_context():
#         driver = get_driver()

#         # Delete the user
#         def delete_user(tx):
#             return tx.run("MATCH (u:User {email: $email}) DETACH DELETE u", email=email).consume()

#         with driver.session() as session:
#             session.execute_write(delete_user)
#             session.close()


def test_authenticate_user(app):
    with app.app_context():
        driver = get_driver()

        # Delete the user
        def delete_user(tx):
            return tx.run("MATCH (u:User {email: $email}) DETACH DELETE u", email=email).consume()

        with driver.session() as session:
            session.execute_write(delete_user)
            session.close()

        # Run the test
        dao = AuthDAO(driver, "secret")

        dao.register(email, password, name)

        output = dao.authenticate(email, password)

        assert output["userId"] is not None
        assert output["name"] == name
        assert "password" not in output
        assert output["userId"] is not None
        assert output["token"] is not None

def test_return_false_incorrect_password(app):
    with app.app_context():
        driver = get_driver()

        dao = AuthDAO(driver, "secret")

        output = dao.authenticate(email, "incorrect")

        assert output is False

def test_return_false_incorrect_username(app):
    with app.app_context():
        driver = get_driver()

        dao = AuthDAO(driver, "secret")
        output = dao.authenticate("unknown@email.com", password)

        assert output is False

def test_set_GA_timestamp_to_verify_test(app):
    def update_user(tx):
        return tx.run("""
            MATCH (u:User {email: $email})
            SET u.authenticatedAt = datetime()
        """, email=email).consume()

    with app.app_context():
        driver = get_driver()

        with driver.session() as session:
            session.execute_write(update_user)