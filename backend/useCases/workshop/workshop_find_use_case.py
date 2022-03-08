import logging
from colorama import Fore
from backend.repositories.mongo.workshop_repository import WorkshopRepository
from backend.requests.workshop.workshop_find_request import WorkshopFindRequest


from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)

logger = logging.getLogger(__name__)

def workshop_find_use_case(repo: WorkshopRepository, request: WorkshopFindRequest) -> ResponseFailure | ResponseSuccess:
    """ Get workshops from the database.
    -------------------------------------------
    Get one workshop o more from the database based in the filters of the 
    WorkshopFindRequest payload. If the WorkshopFindRequest doesn't has
    a payload, return all the workshops in the database.
    Args:
        repo (WorkshopRepository): An instance of the WorkshopRepository class with the method to find the workshop in the DB 
        request (WorkshopFindRequest): An instance of WorkshopFindRequest with the filters of the query.

    Returns:
       ResponseFailure | ResponseSuccess : Return a ResponseSuccess if a workshop was found successfully, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:

        workshop = repo.find_workshop(request.filters)
        
        if not workshop:
            return ResponseFailure(404, "Specialty doesn't exists")

        return ResponseSuccess(workshop)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message="Server Error")
