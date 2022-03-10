import logging
from colorama import Fore
from backend.repositories.mongo.specialty_repository import SpecialtyRepository
from backend.requests.specialty.specialty_find_request import SpecialtyFindRequest


from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)

logger = logging.getLogger(__name__)

def specialty_find_use_case(repo: SpecialtyRepository, request: SpecialtyFindRequest) -> ResponseFailure | ResponseSuccess:
    """ Get specialties from the database.
    -------------------------------------------
    Get one specialty o more from the database based in the filters of the 
    SpecialtyFindRequest payload. If the SpecialtyFindRequest doesn't has
    a payload, return all the specialties in the database.
    Args:
        repo (SpecialtyRepository): An instance of the SpecialtyRepository class with the method to find the specialty in the DB 
        request (SpecialtyFindRequest): An instance of SpecialtyFindRequest with the filters of the query.

    Returns:
       ResponseFailure | ResponseSuccess : Return a ResponseSuccess if a user was found successfully, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:

        specialty = repo.find_specialty(request.filters)
        
        if not specialty:
            return ResponseFailure(404, "Specialty doesn't exists")

        return ResponseSuccess(specialty)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message="Server Error")
