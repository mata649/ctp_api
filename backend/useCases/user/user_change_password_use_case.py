import logging
# External Libs
from colorama import Fore
from backend.helpers.encrypt_password import encrypt_password
from backend.helpers.user_exists import user_exists
from backend.helpers.user_is_authorized import user_is_authorized

from backend.repositories.mongo.user_repository import UserRepository
from backend.requests.user.user_change_password_request import UserChangePasswordRequest
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)



def user_change_password_use_case(repo: UserRepository, request: UserChangePasswordRequest) -> ResponseSuccess | ResponseFailure:
    """Changes a user password in a database.
    ----------------------------------------------------------
    Changes a user password in the database, the UserUpdateRequest has the payload with the 
    user information.
    -------------------------------------------------------------
    Args:
        repo (UserRepository): An instance of the UserRepository class with the method to register the user in the DB. 
        request (UserChangePasswordRequest): An instance of UserChangePasswordRequest with the user information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the update of the user was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")
        
        if not user_exists(id =request.user.id, repo=repo):
            return ResponseFailure(404, "User doesn't exists")
        user = request.user
        user.password = encrypt_password(user.password)
        user = repo.change_user_password(request.user)
        user.password = None
        return ResponseSuccess(user)

        return ResponseFailure(409, "The email is already taken")

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
