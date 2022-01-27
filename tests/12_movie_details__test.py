import pytest

from api.exceptions.notfound import NotFoundException

from api.neo4j import get_driver
from api.dao.movies import MovieDAO

lock_stock = "100"

def test_get_movie_by_id(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = MovieDAO(driver)

        # Find Movie
        output = dao.find_by_id(lock_stock)

        assert output["tmdbId"] == lock_stock

        # Test NotFoundException is raised
        with pytest.raises(NotFoundException):
            dao.find_by_id(9999)

def test_get_similar_movies(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = MovieDAO(driver)

        # Find Similar Movies
        limit = 1

        output = dao.get_similar_movies(lock_stock, limit)

        assert len(output) == limit

        # Check skip is applied
        paginated = dao.get_similar_movies(lock_stock, limit, 1)

        assert len(paginated) == limit
        assert output[0] != paginated[0]

        print("Here is the answer to the quiz question on the lesson:")
        print("What is the title of the most similar movie to Lock, Stock & Two Smoking Barrels?")
        print("Copy and paste the following answer into the text box: \n\n")

        print(output[0]["title"])


