import logging
# External Libs
from colorama import Fore
from backend.helpers.user_exists import user_exists
from backend.helpers.user_is_authorized import user_is_authorized


from backend.repositories.mongo.user_repository import UserRepository
from backend.requests.user.user_update_request import UserUpdateRequest

# Request
from backend.requests.user.user_find_request import build_user_find_request

# UseCases
from backend.useCases.user.user_find_use_case import user_find_use_case



logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def user_update_use_case(repo: UserRepository, request: UserUpdateRequest) -> ResponseSuccess | ResponseFailure:
    """Updates a user in a database.
    ----------------------------------------------------------
    Updates a user in the database, the UserUpdateRequest has the payload with the 
    user information.
    -------------------------------------------------------------
    Args:
        repo (UserRepository): An instance of the UserRepository class with the method to register the user in the DB. 
        request (UserUpdateRequest): An instance of UserUpdateRequest with the user information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the update of the user was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:

        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")

        if not user_exists(id=request.user.id, repo=repo):
            return ResponseFailure(404, "User doesn't exists")

        req_user_by_email = build_user_find_request(
            {"email": request.user.email})
        response_email = user_find_use_case(repo, req_user_by_email)

        if not response_email or response_email.value.id == request.user.id:

            user = repo.update_user(request.user)
            user.password = None
            return ResponseSuccess(user)

        return ResponseFailure(409, "The email is already taken")

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
