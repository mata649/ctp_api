import logging
# External Libs
from colorama import Fore
from backend.helpers.specialty_exists import specialty_exists
from backend.helpers.user_is_authorized import user_is_authorized
from backend.repositories.mongo.specialty_repository import SpecialtyRepository
from backend.requests.specialty.specialty_update_request import SpecialtyUpdateRequest
from backend.requests.request import InvalidRequest
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def specialty_update_use_case(repo: SpecialtyRepository, request: SpecialtyUpdateRequest | InvalidRequest) -> ResponseSuccess | ResponseFailure:
    """Updates a specialty in a database.
    ----------------------------------------------------------
    Updates a specialty in the database, the SpecialtyUpdateRequest has the payload with the 
    specialty information.
    -------------------------------------------------------------
    Args:
        repo (SpecialtyRepository): An instance of the SpecialtyRepository class with the method to update the specialty in the DB. 
        request (SpecialtyUpdateRequest): An instance of SpecialtyUpdateRequest with the specialty information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the update of the specialty was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
     

        specialty = request.specialty
        if not specialty_exists(specialty.id, repo):
            return ResponseFailure(404, "Specialty doesn't exists")

        specialty = repo.update_specialty(specialty)
        return ResponseSuccess(specialty)

    except Exception as err:
        logger.warning(Fore.RED+str(err))
        return ResponseFailure(code=500, message=err)
