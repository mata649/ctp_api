import logging
# External Libs
from colorama import Fore
from backend.helpers.specialty_exists import specialty_exists
from backend.helpers.user_is_authorized import user_is_authorized


from backend.repositories.mongo.specialty_repository import SpecialtyRepository
from backend.requests.specialty.specialty_delete_request import SpecialtyDeleteRequest


logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def specialty_delete_use_case(repo: SpecialtyRepository, request: SpecialtyDeleteRequest) -> ResponseSuccess | ResponseFailure:
    """Deletes a specialty in a database.
    ----------------------------------------------------------
    Deletes a specialty in the database, the SpecialtyDeleteRequest has the payload with the 
    specialty information.
    -------------------------------------------------------------
    Args:
        repo (SpecialtyRepository): An instance of the SpecialtyRepository class with the method to delete the specialty in the DB. 
        request (SpecialtyDeleteRequest): An instance of SpecialtyDeleteRequest with the specialty information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the elimination of the specialty was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:

        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")

        if not specialty_exists(id=request.specialty.id, repo=repo):
            return ResponseFailure(404, "Specialty doesn't exists")

        specialty = repo.delete_specialty(request.specialty)

        return ResponseSuccess(specialty)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
