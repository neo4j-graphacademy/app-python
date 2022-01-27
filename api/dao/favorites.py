from api.data import popular, goodfellas
from api.exceptions.notfound import NotFoundException

class FavoriteDAO:
    """
    The constructor expects an instance of the Neo4j Driver, which will be
    used to interact with Neo4j.
    """
    def __init__(self, driver):
        self.driver=driver


    """
    This method should retrieve a list of movies that have an incoming :HAS_FAVORITE
    relationship from a User node with the supplied `userId`.

    Results should be ordered by the `sort` parameter, and in the direction specified
    in the `order` parameter.

    Results should be limited to the number passed as `limit`.
    The `skip` variable should be used to skip a certain number of rows.
    """
    # tag::all[]
    def all(self, user_id, sort = 'title', order = 'ASC', limit = 6, skip = 0):
        # TODO: Open a new session
        # TODO: Retrieve a list of movies favorited by the user
        return popular
    # end::all[]


    """
    This method should create a `:HAS_FAVORITE` relationship between
    the User and Movie ID nodes provided.
   *
    If either the user or movie cannot be found, a `NotFoundError` should be thrown.
    """
    # tag::add[]
    def add(self, user_id, movie_id):
        # TODO: Open a new Session
        # TODO: Define a new transaction function to create a HAS_FAVORITE relationship
        # TODO: Execute the transaction function within a Write Transaction
        # TODO: Return movie details and `favorite` property

        return {
            **goodfellas,
            "favorite": False
        }
    # end::add[]

    """
    This method should remove the `:HAS_FAVORITE` relationship between
    the User and Movie ID nodes provided.

    If either the user, movie or the relationship between them cannot be found,
    a `NotFoundError` should be thrown.
    """
    # tag::remove[]
    def remove(self, user_id, movie_id):
        # TODO: Open a new Session
        # TODO: Define a transaction function to delete the HAS_FAVORITE relationship within a Write Transaction
        # TODO: Execute the transaction function within a Write Transaction
        # TODO: Return movie details and `favorite` property

        return {
            **goodfellas,
            "favorite": False
        }
    # end::remove[]
