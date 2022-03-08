import logging
# External Libs
from colorama import Fore
from backend.helpers.user_exists import user_exists
from backend.helpers.user_is_authorized import user_is_authorized


from backend.repositories.mongo.user_repository import UserRepository
from backend.requests.user.user_delete_request import UserDeleteRequest


logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def user_delete_use_case(repo: UserRepository, request: UserDeleteRequest) -> ResponseSuccess | ResponseFailure:
    """Deletes a user in a database.
    ----------------------------------------------------------
    Deletes a user in the database, the UserDeleteRequest has the payload with the 
    user information.
    -------------------------------------------------------------
    Args:
        repo (UserRepository): An instance of the UserRepository class with the method to register the user in the DB. 
        request (UserDeleteRequest): An instance of UserDeleteRequest with the user information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the elimination of the user was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:

        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")

        if not user_exists(id=request.user.id, repo=repo):
            return ResponseFailure(404, "User doesn't exists")

        user = repo.delete_user(request.user)
        user.password = None
        return ResponseSuccess(user)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
