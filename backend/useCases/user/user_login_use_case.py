import logging
from colorama import Fore
import bcrypt
from backend.entities.user import User

from backend.repositories.mongo.user_repository import UserRepository

from backend.requests.user.user_login_request import UserLoginRequest
from backend.requests.user.user_find_request import  build_user_find_request
from backend.useCases.user.user_find_use_case import user_find_use_case




logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def decrypt_password(hashed_password:str, plain_text_password:str) -> bool:
    """Decrypt the encrypted password provided.
    ----------------------------------------------------------
    Check if an encrypted password matches a plaintext password.
    Args:
        hashed_password (str): The encrypted password.
        plain_text_password (str): The plain text password. 

    Returns:
        bool: Return a True if the password matches, else return False 
    """
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def user_login_use_case(repo: UserRepository, request: UserLoginRequest) -> ResponseSuccess | ResponseFailure:
    """Authenticates a user from the database.
    ---------------------------------------------
    Checks if a user can be authenticated based in the email and password, 
    the UserLoginRequest has the payload with the email and password

    Args:
        repo (UserRepository): An instance of the UserRepository class with the method to authenticate the user in the DB 
        request (UserLoginRequest): An instance of UserLoginRequest with the email and password.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the authentication was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
        req_user_by_email = build_user_find_request(
            {"email": request.user.email})

        response_email = user_find_use_case(repo, req_user_by_email)
        if not response_email:
            return ResponseFailure(code=409, message="Username or password are incorrects")
        
        user: User = response_email.value
        if not decrypt_password(user.password, request.user.password):
            return ResponseFailure(code=409, message="Username or password are incorrects")
        user.password = ''
        return ResponseSuccess(user)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message="Server Error")