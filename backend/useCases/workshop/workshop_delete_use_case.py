import logging
# External Libs
from colorama import Fore
from backend.helpers.workshop_exists import workshop_exists
from backend.helpers.user_is_authorized import user_is_authorized


from backend.repositories.mongo.workshop_repository import WorkshopRepository
from backend.requests.workshop.workshop_delete_request import WorkshopDeleteRequest

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def workshop_delete_use_case(repo: WorkshopRepository, request: WorkshopDeleteRequest) -> ResponseSuccess | ResponseFailure:
    """Deletes a workshop in a database.
    ----------------------------------------------------------
    Deletes a workshop in the database, the WorkshopDeleteRequest has the payload with the 
    workshop information.
    -------------------------------------------------------------
    Args:
        repo (WorkshopRepository): An instance of the WorkshopRepository class with the method to delete the workshop in the DB. 
        request (WorkshopDeleteRequest): An instance of WorkshopDeleteRequest with the workshop information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the elimination of the workshop was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:

        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")

        if not workshop_exists(id=request.workshop.id, repo=repo):
            return ResponseFailure(404, "Workshop doesn't exists")

        workshop = repo.delete_workshop(request.workshop)
        
        return ResponseSuccess(workshop)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
