import pytest
from api.exceptions.notfound import NotFoundException

from api.neo4j import get_driver
from api.dao.favorites import FavoriteDAO
from api.dao.movies import MovieDAO

toy_story = '862'
goodfellas = '769'
user_id = 'fe770c6b-4034-4e07-8e40-2f39e7a6722c'
email = 'graphacademy.flag@neo4j.com'

@pytest.fixture(autouse=True)
def before_all(app):
    with app.app_context():
        driver = get_driver()

        with driver.session() as session:
            session.write_transaction(lambda tx: tx.run("""
                MERGE (u:User {userId: $userId})
                SET u.email = $email
                FOREACH (r in [ (u)-[r:HAS_FAVORITE]->() | r ] | DELETE r)
            """, userId = user_id, email=email))


def test_return_positive_flag_on_all(app):
    with app.app_context():
        driver = get_driver()

        movies = MovieDAO(driver)
        favorites = FavoriteDAO(driver)

        # Find the top rated movie
        [ first ] = movies.all('imdbRating', 'DESC', 1, 0, user_id)

        first_id = first["tmdbId"]

        assert first["favorite"] == False

        # Add to favorites
        add = favorites.add(user_id, first_id)

        assert add["tmdbId"] == first_id
        assert add["favorite"] == True

        # Check updated `all` call
        [ after_all_first ] = movies.all('imdbRating', 'DESC', 1, 0, user_id)

        assert after_all_first["tmdbId"] == first_id
        assert after_all_first["favorite"] == True

