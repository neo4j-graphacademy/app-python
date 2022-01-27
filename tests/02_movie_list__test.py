import pytest

from api.neo4j import close_driver, get_driver
from api.dao.movies import MovieDAO

def test_pagination(app):
    """Test that the all method on the MovieDAO is correctly implemented"""
    with app.app_context():
        driver = get_driver()

        dao = MovieDAO(driver)

        first = dao.all("title", "ASC", 1, 0)
        second = dao.all("title", "ASC", 1, 1)

        assert len(first) is 1
        assert len(second) is 1

        assert first[0] is not second[0]


def test_ordering(app):
    """Test that the ordering is correctly implemented"""
    with app.app_context():
        driver = get_driver()

        dao = MovieDAO(driver)

        ordered_by_title = dao.all("title", "ASC", 1, 0)

        first = dao.all("imdbRating", "DESC", 1, 0)
        second = dao.all("imdbRating", "DESC", 1, 1)
        ascending = dao.all("imdbRating", "ASC", 1, 0)

        assert len(first) is 1
        assert len(second) is 1
        assert len(ascending) is 1

        assert first[0] is not second[0]
        assert first[0] is not ordered_by_title[0]
        assert first[0] is not ascending[0]

        print("Here is the answer to the quiz question on the lesson:")
        print("What is the title of the highest rated movie in the recommendations dataset?")
        print("Copy and paste the following answer into the text box:")
        print("")

        print(first[0]["title"])


