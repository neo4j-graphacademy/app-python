from api.data import people, pacino
from api.exceptions.notfound import NotFoundException


class PeopleDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """

    def __init__(self, driver):
        self.driver = driver

    """
    This method should return a paginated list of People (actors or directors),
    with an optional filter on the person's name based on the `q` parameter.

    Results should be ordered by the `sort` parameter and limited to the
    number passed as `limit`.  The `skip` variable should be used to skip a
    certain number of rows.
    """
    # tag::all[]
    def all(self, q, sort = 'name', order = 'ASC', limit = 6, skip = 0):
        # Get a list of people from the database
        def get_all_people(tx, q, sort, order, limit, skip):
            cypher = "MATCH (p:Person) "

            # If q is set, use it to filter on the name property
            if q is not None:
                cypher += "WHERE p.name CONTAINS $q"

            cypher += """
            RETURN p {{ .* }} AS person
            ORDER BY p.`{0}` {1}
            SKIP $skip
            LIMIT $limit
            """.format(sort, order)

            result = tx.run(cypher, q=q, sort=sort, order=order, limit=limit, skip=skip)

            return [ row.get("person") for row in result ]

        with self.driver.session() as session:
            return session.execute_read(get_all_people, q, sort, order, limit, skip)
    # end::all[]

    """
    Find a user by their ID.

    If no user is found, a NotFoundError should be thrown.
    """
    # tag::findById[]
    def find_by_id(self, id):
        # TODO: Find a user by their ID

        return pacino

    # end::findById[]

    """
    Get a list of similar people to a Person, ordered by their similarity score
    in descending order.
    """
    # tag::getSimilarPeople[]
    def get_similar_people(self, id, limit = 6, skip = 0):
        # TODO: Get a list of similar people to the person by their id

        return people[skip:limit]
    # end::getSimilarPeople[]