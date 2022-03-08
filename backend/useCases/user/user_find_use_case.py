import logging
from colorama import Fore
from backend.entities.user import User
from backend.repositories.mongo.user_repository import UserRepository
from backend.requests.user.user_find_request import UserFindRequest


logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def user_find_use_case(repo: UserRepository, request: UserFindRequest) -> ResponseFailure | ResponseSuccess:
    """ Get users from the database.
    -------------------------------------------
    Get one user o more from the database based in the filters of the 
    UserFindRequest payload. If the UserFindRequest doesn't has
    a payload, return all the users in the database.
    Args:
        repo (UserRepository): An instance of the UserRepository class with the method to find the user in the DB 
        request (UserFindRequest): An instance of UserFindRequest with the filters of the query.

    Returns:
       ResponseFailure | ResponseSuccess : Return a ResponseSuccess if a user was found successfully, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
        
        user = repo.find_user(request.filters)
    
        if not user :
            return ResponseFailure(404, "User doesn't exists")
            
        return ResponseSuccess(user)
        
    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message="Server Error")