import logging
# External Libs
from colorama import Fore
from backend.helpers.user_is_authorized import user_is_authorized
from backend.repositories.mongo.specialty_repository import SpecialtyRepository
from backend.requests.specialty.specialty_create_request import SpecialtyCreateRequest
from backend.requests.request import InvalidRequest

logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def specialty_create_use_case(repo: SpecialtyRepository, request: SpecialtyCreateRequest | InvalidRequest) -> ResponseSuccess | ResponseFailure:
    """Creates a specialty in a database.
    ----------------------------------------------------------
    Creates a specialty in the database, the SpecialtyCreateRequest has the payload with the 
    specialty information.
    -------------------------------------------------------------
    Args:
        repo (SpecialtyRepository): An instance of the SpecialtyRepository class with the method to register the specialty in the DB. 
        request (SpecialtyCreateRequest): An instance of SpecialtyCreateRequest with the specialty information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the register of the specialty was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
        
        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")
        
        specialty = repo.create_specialty(request.specialty)
        
        return ResponseSuccess(specialty)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
