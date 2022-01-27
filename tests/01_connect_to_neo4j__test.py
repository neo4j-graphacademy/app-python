import os
from api.neo4j import close_driver, get_driver

def test_env_vars():
    """Test that environment variables have been set"""

    assert "NEO4J_URI" in os.environ
    assert "NEO4J_USERNAME" in os.environ
    assert "NEO4J_PASSWORD" in os.environ


def test_driver_initiated(app):
    """Test that driver has been set against current_app"""
    with app.app_context():
        assert app.driver is not None


def test_can_get_driver(app):
    """Test that get_driver returns the driver instance"""
    with app.app_context():
        driver = get_driver()

        assert driver is not None


def test_can_close_driver(app):
    """Test that the driver can be closed"""
    with app.app_context():
        driver = close_driver()

        assert driver is None