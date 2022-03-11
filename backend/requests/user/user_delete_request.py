from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.user import User


class UserDeleteRequest(ValidRequest):
    def __init__(self, user: User, current_id: str) -> None:
        self.user = user
        self.current_id = current_id



def build_user_delete_request(user: User, current_id: str) -> InvalidRequest | UserDeleteRequest:
    """Validates a UserDeleteRequest information.
    --------------------------------------------------------
    Validates that the current_id and user id attributes meet the requirements of the request.
    --------------------------------------------------------
    Args:
        user (User): A User entity with id attribute.
        current_id (str): id of the user making the request 
    ---------------------------------------------------------
    Returns:
        InvalidRequest | UserDeleteRequest: Return an UserDeleteRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()
   
    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not user.id:
        invalid_request.add_error("user_id", "user_id is necessary")

    if invalid_request.has_error():
        return invalid_request

    return UserDeleteRequest(user, current_id)
