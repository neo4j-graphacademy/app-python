from api.data import popular, goodfellas

from api.exceptions.notfound import NotFoundException
from api.data import popular

class MovieDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver = driver

    """
     This method should return a paginated list of movies ordered by the `sort`
     parameter and limited to the number passed as `limit`.  The `skip` variable should be
     used to skip a certain number of rows.

     If a user_id value is suppled, a `favorite` boolean property should be returned to
     signify whether the user has added the movie to their "My Favorites" list.
    """
    # tag::all[]
    def all(self, sort, order, limit=6, skip=0, user_id=None):
        # TODO: Get list from movies from Neo4j
        return popular
    # end::all[]

    """
    This method should return a paginated list of movies that have a relationship to the
    supplied Genre.

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.
    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.

    If a user_id value is suppled, a `favorite` boolean property should be returned to
    signify whether the user has added the movie to their "My Favorites" list.
    """
    # tag::getByGenre[]
    def get_by_genre(self, name, sort='title', order='ASC', limit=6, skip=0, user_id=None):
        # TODO: Get Movies in a Genre
        # TODO: The Cypher string will be formated so remember to escape the braces: {{name: $name}}
        # MATCH (m:Movie)-[:IN_GENRE]->(:Genre {name: $name})

        return popular[skip:limit]
    # end::getByGenre[]

    """
    This method should return a paginated list of movies that have an ACTED_IN relationship
    to a Person with the id supplied

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.
    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.

    If a user_id value is suppled, a `favorite` boolean property should be returned to
    signify whether the user has added the movie to their "My Favorites" list.
    """
    # tag::getForActor[]
    def get_for_actor(self, id, sort='title', order='ASC', limit=6, skip=0, user_id=None):
        # TODO: Get Movies for an Actor
        # TODO: The Cypher string will be formated so remember to escape the braces: {{tmdbId: $id}}
        # MATCH (:Person {tmdbId: $id})-[:ACTED_IN]->(m:Movie)

        return popular[skip:limit]
    # end::getForActor[]

    """
    This method should return a paginated list of movies that have an DIRECTED relationship
    to a Person with the id supplied

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.
    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.

    If a user_id value is suppled, a `favorite` boolean property should be returned to
    signify whether the user has added the movie to their "My Favorites" list.
    """
    # tag::getForDirector[]
    def get_for_director(self, id, sort='title', order='ASC', limit=6, skip=0, user_id=None):
        # TODO: Get Movies directed by a Person
        # TODO: The Cypher string will be formated so remember to escape the braces: {{name: $name}}
        # MATCH (:Person {tmdbId: $id})-[:DIRECTED]->(m:Movie)

        return popular[skip:limit]
    # end::getForDirector[]

    """
    This method find a Movie node with the ID passed as the `id` parameter.
    Along with the returned payload, a list of actors, directors, and genres should
    be included.
    The number of incoming RATED relationships should also be returned as `ratingCount`

    If a user_id value is suppled, a `favorite` boolean property should be returned to
    signify whether the user has added the movie to their "My Favorites" list.
    """
    # tag::findById[]
    def find_by_id(self, id, user_id=None):
        # TODO: Find a movie by its ID
        # MATCH (m:Movie {tmdbId: $id})

        return goodfellas
    # end::findById[]

    """
    This method should return a paginated list of similar movies to the Movie with the
    id supplied.  This similarity is calculated by finding movies that have many first
    degree connections in common: Actors, Directors and Genres.

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.
    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.

    If a user_id value is suppled, a `favorite` boolean property should be returned to
    signify whether the user has added the movie to their "My Favorites" list.
    """
    # tag::getSimilarMovies[]
    def get_similar_movies(self, id, limit=6, skip=0, user_id=None):
        # TODO: Get similar movies from Neo4j

        return popular[skip:limit]
    # end::getSimilarMovies[]


    """
    This function should return a list of tmdbId properties for the movies that
    the user has added to their 'My Favorites' list.
    """
    # tag::getUserFavorites[]
    def get_user_favorites(self, tx, user_id):
        return []
    # end::getUserFavorites[]
