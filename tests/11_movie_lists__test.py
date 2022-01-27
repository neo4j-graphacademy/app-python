import pytest

from api.neo4j import get_driver
from api.dao.movies import MovieDAO

tom_hanks = '31'
coppola = '1776'
limit = 10
sort = "title"
order = "ASC"

def test_paginated_list_of_movies_by_genre(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = MovieDAO(driver)

        genre = "Comedy"

        # Get List
        output = dao.get_by_genre(genre, sort, order, limit, 0)

        assert len(output) == limit

        # With skip
        paginated = dao.get_by_genre(genre, sort, order, limit, 1)

        assert len(paginated) == limit
        assert output[0] != paginated[0]

        # Reordered
        reordered = dao.get_by_genre(genre, 'released', order, limit, 0)

        assert len(reordered) == limit
        assert output[0] != reordered[0]

def test_paginated_list_of_movies_for_actor(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = MovieDAO(driver)

        # Get List
        output = dao.get_for_actor(tom_hanks, sort, order, limit, 0)

        assert len(output) == limit

        # With skip
        paginated = dao.get_for_actor(tom_hanks, sort, order, limit, 1)

        assert len(paginated) == limit
        assert output[0] != paginated[0]

        # Reordered
        reordered = dao.get_for_actor(tom_hanks, 'released', order, limit, 0)

        assert len(reordered) == limit
        assert output[0] != reordered[0]


def test_paginated_list_of_movies_for_director(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = MovieDAO(driver)


        # Get List
        output = dao.get_for_director(tom_hanks, sort, order, limit, 0)

        # Tom Hanks has directed two films in the dataset
        assert len(output) == 2

        # With skip
        paginated = dao.get_for_director(tom_hanks, sort, order, limit, 1)

        assert len(paginated) == 1
        assert output[0] != paginated[0]

        # Reordered
        reordered = dao.get_for_director(tom_hanks, 'released', order, limit, 0)

        assert len(reordered) == 2
        assert output[0] != reordered[0]

def test_find_coppola_films(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = MovieDAO(driver)

        output = dao.get_for_director(coppola, sort, order, 99)

        assert len(output) == 16

        print("Here is the answer to the quiz question on the lesson:")
        print("How many films has Francis Ford Coppola directed?")
        print("Copy and paste the following answer into the text box: \n\n")

        print(len(output))

