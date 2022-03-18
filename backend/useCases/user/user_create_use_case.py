import logging
# External Libs

from colorama import Fore
from backend.helpers.encrypt_password import encrypt_password
from backend.helpers.user_is_authorized import user_is_authorized

from backend.repositories.mongo.user_repository import UserRepository
from backend.requests.request import InvalidRequest
from backend.requests.user.user_create_request import UserCreateRequest

# Request
from backend.requests.user.user_find_request import build_user_find_request

# UseCases
from backend.useCases.user.user_find_use_case import user_find_use_case
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)





def user_create_use_case(repo: UserRepository, request: UserCreateRequest | InvalidRequest) -> ResponseSuccess | ResponseFailure:
    """Creates a user in a database.
    ----------------------------------------------------------
    Creates a user in the database, the UserCreateRequest has the payload with the 
    user information.
    -------------------------------------------------------------
    Args:
        repo (UserRepository): An instance of the UserRepository class with the method to register the user in the DB. 
        request (UserCreateRequest): An instance of UserCreateRequest with the user information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the register of the user was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
        
        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")
        
        req_user_by_email = build_user_find_request(
            {"email": request.user.email})

        response_email = user_find_use_case(repo, req_user_by_email)

        if not response_email:
            user = request.user
            user.password = encrypt_password(user.password)
            user.email = user.email.lower()
            user = repo.create_user(user)
            user.password = None
            return ResponseSuccess(user)

        return ResponseFailure(409, "The email is already taken")

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
