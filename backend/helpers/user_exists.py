from backend.repositories.mongo.UserRepository import UserRepository
from backend.requests.user.user_find_request import build_user_find_request
from backend.useCases.user.user_find_use_case import user_find_use_case


def user_exists(id: str, repo: UserRepository) -> bool:
    """Checks if a user exists in the database, based in a user id

    Args:
        id (str): The id of the user.
        repo (UserRepository): An instance of a UserRepository object.

    Returns:
        bool: Returns True if the user exists, else return False
    """
    req_user_by_id = build_user_find_request(
            {"id": id})
    response = user_find_use_case(repo, req_user_by_id)

    if response and response.value.enable:
        return True
    return False