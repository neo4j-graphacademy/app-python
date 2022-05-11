from api.data import goodfellas, ratings
from api.exceptions.notfound import NotFoundException


class RatingDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """

    def __init__(self, driver):
        self.driver = driver

    """
    Add a relationship between a User and Movie with a `rating` property.
    The `rating` parameter should be converted to a Neo4j Integer.
    """
    # tag::add[]

    def add(self, user_id, movie_id, rating):
        # TODO: Create function to save the rating in the database
        def add_rating(tx, user_id, movie_id, rating):
            cypher = """
            MATCH (u:User {userId: $user_id}), (m:Movie {tmdbId: $movie_id})
            MERGE (u)-[r:RATED]->(m)
            SET r.rating = $rating,
                r.timestamp = timestamp()

            RETURN m {
                .*,
                rating: r.rating
            } AS movie
            """
            return tx.run(cypher, user_id=user_id, movie_id=movie_id, rating=rating).single()
        # TODO: Call the function within a write transaction
        with self.driver.session() as session:
            result = session.write_transaction(
                add_rating, user_id, movie_id, rating)
        # TODO: Return movie details along with a rating
            if result is None:
                raise NotFoundException()

            return result['movie']

    # end::add[]

    """
    Return a paginated list of reviews for a Movie.

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.
    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.
    """
    # tag::forMovie[]

    def for_movie(self, id, sort='timestamp', order='ASC', limit=6, skip=0):
        # TODO: Get ratings for a Movie
        # TODO: Remember to escape the braces in the cypher query with double braces: {{ }}

        return ratings
    # end::forMovie[]
