import logging
# External Libs
from colorama import Fore
from backend.helpers.workshop_exists import workshop_exists
from backend.helpers.user_is_authorized import user_is_authorized
from backend.repositories.mongo.workshop_repository import WorkshopRepository
from backend.requests.workshop.workshop_update_request import WorkshopUpdateRequest
from backend.requests.request import InvalidRequest
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def workshop_update_use_case(repo: WorkshopRepository, request: WorkshopUpdateRequest | InvalidRequest) -> ResponseSuccess | ResponseFailure:
    """Updates a workshop in a database.
    ----------------------------------------------------------
    Updates a workshop in the database, the WorkshopUpdateRequest has the payload with the 
    workshop information.
    -------------------------------------------------------------
    Args:
        repo (WorkshopRepository): An instance of the WorkshopRepository class with the method to update the workshop in the DB. 
        request (WorkshopUpdateRequest): An instance of WorkshopUpdateRequest with the workshop information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the update of the workshop was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
     
        workshop = request.workshop
        if not workshop_exists(workshop.id, repo):
            return ResponseFailure(404, "Workshop doesn't exists")

        workshop = repo.update_workshop(workshop)
        return ResponseSuccess(workshop)

    except Exception as err:
        logger.warning(Fore.RED+str(err))
        return ResponseFailure(code=500, message=err)
