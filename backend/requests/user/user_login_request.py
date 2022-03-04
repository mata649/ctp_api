
from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.user import User


class UserLoginRequest(ValidRequest):
    def __init__(self, user: User) -> None:
        self.user = user


def build_user_login_request(user: User) -> InvalidRequest | UserLoginRequest:
    """Validates a UserLoginRequest information.
    -----------------------------------------------------
    Validates that the email and password attributes meet 
    the requirements of the request.
    ----------------------------------------------------- 
    Args:
        user (User): A User entity with password and email attributes.  
    ----------------------------------------------------- 
    Returns:
        InvalidRequest | UserLoginRequest: Return an UserLoginRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    
    
    invalid_request = InvalidRequest()

    if not user.email:
        invalid_request.add_error("email", "The email is necessary")

    if not user.password:
        invalid_request.add_error("password", "The password is necessary")

    if invalid_request.has_error():

        return invalid_request

    return UserLoginRequest(user)
