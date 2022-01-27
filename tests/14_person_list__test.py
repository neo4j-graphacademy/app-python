import pytest

from api.neo4j import get_driver
from api.dao.people import PeopleDAO


def test_should_return_paginated_list_of_people(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = PeopleDAO(driver)

        # Get List
        limit = 1

        first_page = dao.all(None, "name", "ASC", limit, 0)

        assert len(first_page) == 1

        second_page = dao.all(None, "name", "ASC", limit, 1)

        assert len(second_page) == 1
        assert first_page != second_page

        descending =  dao.all(None, "name", "DESC", limit, 0)

        assert len(descending) == 1
        assert first_page != descending
        assert second_page != descending


def test_apply_query_filter(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = PeopleDAO(driver)

        # Get Filtered List
        q = "Ab"
        limit = 10

        first = dao.all(q, "name", "ASC", limit)
        last = dao.all(q, "name", "DESC", limit)

        assert len(first) == limit
        assert len(last) == limit
        assert first != last

        # Check filtering worked
        assert "Ab" in first[0]["name"]
        assert "Ab" in last[0]["name"]


def test_get_outcome(app):
    with app.app_context():
        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = PeopleDAO(driver)

        first = dao.all(None, "name", "ASC", 1)

        print("Here is the answer to the quiz question on the lesson:")
        print("What is the name of the first person in the database in alphabetical order?")
        print("Copy and paste the following answer into the text box: \n\n")

        print(first[0]["name"])

