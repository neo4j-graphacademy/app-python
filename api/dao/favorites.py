import neo4j

from api.data import goodfellas, popular
from api.exceptions.notfound import NotFoundException


class FavoriteDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """

    def __init__(self, driver):
        self.driver: neo4j.Neo4jDriver = driver

    """
    This method should retrieve a list of movies that have an incoming :HAS_FAVORITE
    relationship from a User node with the supplied `userId`.

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.

    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.
    """
    # tag::all[]

    def all(self, user_id, sort='title', order='ASC', limit=6, skip=0):
        with self.driver.session() as session:
            # Retrieve a list of movies favorited by the user
            movies = session.read_transaction(lambda tx: tx.run("""
                MATCH (u:User {{userId: $userId}})-[r:HAS_FAVORITE]->(m:Movie)
                RETURN m {{
                    .*,
                    favorite: true
                }} AS movie
                ORDER BY m.`{0}` {1}
                SKIP $skip
                LIMIT $limit
            """.format(sort, order), userId=user_id, limit=limit, skip=skip).value("movie"))

            return movies
    # end::all[]

    """
    This method should create a `:HAS_FAVORITE` relationship between
    the User and Movie ID nodes provided.
   *
    If either the user or movie cannot be found, a `NotFoundError` should be thrown.
    """
    # tag::add[]

    def add(self, user_id, movie_id):
        # Define a new transaction function to create a HAS_FAVORITE relationship

        def add_to_favorites(tx, user_id, movie_id):
            row = tx.run("""
                MATCH (u:User {userId: $userId})
                MATCH (m:Movie {tmdbId: $movieId})

                MERGE (u)-[r:HAS_FAVORITE]->(m)
                ON CREATE SET u.createdAt = datetime()

                RETURN m {
                    .*,
                    favorite: true
                } AS movie
            """, userId=user_id, movieId=movie_id).single()

            # If no rows are returnedm throw a NotFoundException
            if row == None:
                raise NotFoundException()

            return row.get("movie")

        with self.driver.session() as session:
            return session.write_transaction(add_to_favorites, user_id, movie_id)
    # end::add[]

    """
    This method should remove the `:HAS_FAVORITE` relationship between
    the User and Movie ID nodes provided.

    If either the user, movie or the relationship between them cannot be found,
    a `NotFoundError` should be thrown.
    """
    # tag::remove[]

    def remove(self, user_id, movie_id):
        # Define a transaction function to delete the HAS_FAVORITE relationship within a Write Transaction
        def remove_from_favorites(tx, user_id, movie_id):
            row = tx.run("""
                MATCH (u:User {userId: $userId})-[r:HAS_FAVORITE]->(m:Movie {tmdbId: $movieId})
                DELETE r

                RETURN m {
                    .*,
                    favorite: false
                } AS movie
            """, userId=user_id, movieId=movie_id).single()

            # If no rows are returnedm throw a NotFoundException
            if row == None:
                raise NotFoundException()

            return row.get("movie")

        # Execute the transaction function within a Write Transaction
        with self.driver.session() as session:
            # Return movie details and `favorite` property
            return session.write_transaction(remove_from_favorites, user_id, movie_id)
    # end::remove[]
