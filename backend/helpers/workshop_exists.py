from backend.repositories.mongo.workshop_repository import WorkshopRepository
from backend.requests.workshop.workshop_find_request import build_workshop_find_request
from backend.useCases.workshop.workshop_find_use_case import workshop_find_use_case

def workshop_exists(id: str, repo: WorkshopRepository) -> bool:
    """Checks if a workshop exists in the database, based in the workshop id

    Args:
        id (str): The id of the workshop.
        repo (WorkshopRepository): An instance of a WorkshopRepository object.

    Returns:
        bool: Returns True if the workshop exists, else return False
    """
    
    req_workshop_by_id = build_workshop_find_request(
            {"id": id})
    response = workshop_find_use_case(repo, req_workshop_by_id)

    if response and response.value.enable:
        return True
    return False