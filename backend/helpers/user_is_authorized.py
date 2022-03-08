from ast import Return

from backend.entities.roles import Roles
from backend.repositories.mongo.user_repository import UserRepository
from backend.requests.user.user_find_request import build_user_find_request
from backend.useCases.user.user_find_use_case import user_find_use_case
from backend.repositories import userRepo

def  user_is_authorized(id: str) -> bool:
    """Return if a user is authorized.

    Args:
        id (str): The user id
        repo (UserRepository): A instance of a UserRepository object.
    Returns:
        bool: Return true if the user has the role admin or super admin,
        else return false.
    """
    req_user_by_id = build_user_find_request(
        {"id": id})

    resp_user_by_id = user_find_use_case(userRepo, req_user_by_id)

    if not resp_user_by_id:
        return False

    user_found = resp_user_by_id.value
    if user_found.role not in [Roles.ADMIN, Roles.SUPERADMIN]:
        return False
    return True
