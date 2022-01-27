import pytest

from api.exceptions.notfound import NotFoundException

from api.neo4j import get_driver
from api.dao.ratings import RatingDAO

pulp_fiction = "680"

def test_get_movie_ratings(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = RatingDAO(driver)

        # Get Ratings
        limit = 1

        # Descending Order
        descending = dao.for_movie(pulp_fiction, 'timestamp', 'DESC', limit)

        assert len(descending) == limit

        # Check Pagination & Ordering
        ascending = dao.for_movie(pulp_fiction, 'timestamp', 'ASC', limit)

        assert len(ascending) == limit
        assert descending[0] != ascending[0]


        print("\n\n")
        print("Here is the answer to the quiz question on the lesson:")
        print("What is the name of the first person to rate the movie Pulp Fiction?")
        print("Copy and paste the following answer into the text box: \n\n")

        print(ascending[0]["user"]["name"])
