import logging
# External Libs
from colorama import Fore
from backend.helpers.user_is_authorized import user_is_authorized
from backend.repositories.mongo.workshop_repository import WorkshopRepository
from backend.requests.workshop.workshop_create_request import WorkshopCreateRequest
from backend.requests.request import InvalidRequest

logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def workshop_create_use_case(repo: WorkshopRepository, request: WorkshopCreateRequest | InvalidRequest) -> ResponseSuccess | ResponseFailure:
    """Creates a workshop in a database.
    ----------------------------------------------------------
    Creates a workshop in the database, the WorkshopCreateRequest has the payload with the 
    workshop information.
    -------------------------------------------------------------
    Args:
        repo (WorkshopRepository): An instance of the WorkshopRepository class with the method to register the workshop in the DB. 
        request (WorkshopCreateRequest): An instance of WorkshopCreateRequest with the workshop information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the register of the workshop was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
        
        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")
        
        workshop = repo.create_workshop(request.workshop)
        
        return ResponseSuccess(workshop)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
