from password_validator import PasswordValidator
from email_validator import validate_email, EmailNotValidError
from backend.entities.roles import Roles

from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.user import User


class UserCreateRequest(ValidRequest):
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


def is_valid_email(email: str) -> bool:
    """Validates if a string is a valid email.

    Args:
        email (str): A string to validate if is a valid email.

    Returns:
        bool: Return True if the string is a valid email, else return False. 
    """
    try:
        valid = validate_email(email)
        email = valid.email
        return True
    except EmailNotValidError as e:
        return False


def build_user_create_request(user: User, current_id: str) -> InvalidRequest | UserCreateRequest:
    """Validates a UserCreateRequest information.
    -----------------------------------------------------
    Validates that the full_name, email, password and rol attributes meet 
    the requirements of the request.
    ----------------------------------------------------- 
    Args:
        user (User): A User entity with full_name, password, rol and email attributes.
        current_id (str): id of the user making the request 
    ----------------------------------------------------- 
    Returns:
        InvalidRequest | UserCreateRequest: Return an UserCreateRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()
    roles = [Roles.GENERAL, Roles.ADMIN]

    if not is_valid_password(user.password):
        invalid_request.add_error("password", "invalid password")

    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not user.full_name:
        invalid_request.add_error("full_name", "The full_name is necessary")

    if user.role not in roles:
        invalid_request.add_error("rol", "The rol doesn't exists")

    if not is_valid_email(user.email):
        invalid_request.add_error("email", "Incorrect email")

    if invalid_request.has_error():
        return invalid_request

    return UserCreateRequest(user, current_id)
