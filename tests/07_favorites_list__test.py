import pytest
from api.exceptions.notfound import NotFoundException

from api.neo4j import get_driver
from api.dao.favorites import FavoriteDAO

toy_story = '862'
goodfellas = '769'
user_id = '9f965bf6-7e32-4afb-893f-756f502b2c2a'
email = 'graphacademy.favorite@neo4j.com'

@pytest.fixture(autouse=True)
def before_all(app):
    with app.app_context():
        driver = get_driver()

        with driver.session() as session:
            session.execute_write(lambda tx: tx.run("""
                MERGE (u:User {userId: $userId})
                SET u.email = $email
            """, userId = user_id, email=email))


def test_add_raises_error_when_movie_not_found(app):
    with app.app_context():
        driver = get_driver()

        dao = FavoriteDAO(driver)

        with pytest.raises(NotFoundException):
            dao.add(user_id, 9999)


def test_should_add_movie_to_user_favorites(app):
    with app.app_context():
        driver = get_driver()

        dao = FavoriteDAO(driver)

        # Check output
        output = dao.add(user_id, toy_story)

        assert output["tmdbId"] == toy_story
        assert output["favorite"] == True

        # Check list of all
        all = dao.all(user_id)

        assert len([m for m in all if m["tmdbId"] == toy_story]) == 1

def test_remove_raises_error_when_movie_not_found(app):
    with app.app_context():
        driver = get_driver()

        dao = FavoriteDAO(driver)

        with pytest.raises(NotFoundException):
            dao.remove(user_id, 9999)

def test_should_remove_movie_from_user_favorites(app):
    with app.app_context():
        driver = get_driver()

        dao = FavoriteDAO(driver)

        add = dao.add(user_id, goodfellas)

        assert add["tmdbId"] == goodfellas
        assert add["favorite"] == True

        # Check output
        remove = dao.remove(user_id, goodfellas)

        assert remove["tmdbId"] == goodfellas
        assert remove["favorite"] == False

        # Check removed from all list
        all = dao.all(user_id)

        assert len([m for m in all if m["tmdbId"] == goodfellas]) == 0

