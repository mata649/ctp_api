from password_validator import PasswordValidator

from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.user import User


class UserChangePasswordRequest(ValidRequest):
    def __init__(self, user: User, current_id: str) -> None:
        self.user = user
        self.current_id = current_id


def is_valid_password(password: str) -> bool:
    """ Validates if a password meets with the specified schema.
    --------------------------------------------------------
    Validates that the string have 8 characters min, 64 max, a uppercase, 
    a lowercase and a digit.
    Args:
        password (str): A string to validate if meets the requirements of the schema.

    Returns:
        bool: Returns True if the string meets the requirements, else return False.
    """
    schema = PasswordValidator()
    schema\
        .min(8)\
        .max(64)\
        .has().uppercase()\
        .has().lowercase()\
        .has().digits()

    return schema.validate(password)


def build_user_change_password_request(user: User, current_id: str) -> InvalidRequest | UserChangePasswordRequest:
    """Validates a UserChangePasswordRequest information.
    -----------------------------------------------------
    Validates that the password and id attributes meet the requirements of the request.
    ----------------------------------------------------- 
    Args:
        user (User): A User entity with password and id attributes.
        current_id (str): id of the user making the request 
    ----------------------------------------------------- 
    Returns:
        InvalidRequest | UserChangePasswordRequest: Return an UserChangePasswordRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()
   

    if not is_valid_password(user.password):
        invalid_request.add_error("password", "invalid password")

    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not user.id:
        invalid_request.add_error("user_id", "user_id is necessary")

    if invalid_request.has_error():
        return invalid_request

    return UserChangePasswordRequest(user, current_id)
