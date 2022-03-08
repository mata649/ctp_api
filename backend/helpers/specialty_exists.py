from backend.repositories.mongo.specialty_repository import SpecialtyRepository
from backend.requests.specialty.specialty_find_request import build_specialty_find_request
from backend.useCases.specialty.specialty_find_use_case import specialty_find_use_case

def specialty_exists(id: str, repo: SpecialtyRepository) -> bool:
    """Checks if a specialty exists in the database, based in the specialty id

    Args:
        id (str): The id of the specialty.
        repo (SpecialtyRepository): An instance of a SpecialtyRepository object.

    Returns:
        bool: Returns True if the specialty exists, else return False
    """
    
    req_specialty_by_id = build_specialty_find_request(
            {"id": id})
    response = specialty_find_use_case(repo, req_specialty_by_id)

    if response and response.value.enable:
        return True
    return False