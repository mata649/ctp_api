from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.specialty import Specialty


class SpecialtyDeleteRequest(ValidRequest):
    def __init__(self, specialty: Specialty, current_id: str) -> None:
        self.specialty = specialty
        self.current_id = current_id



def build_specialty_delete_request(specialty: Specialty, current_id: str) -> InvalidRequest | SpecialtyDeleteRequest:
    """Validates a SpecialtyDeleteRequest information.
    --------------------------------------------------------
    Validates that the current_id and specialty id attributes meet the requirements of the request.
  
    Args:
        specialty (Specialty): A Specialty entity with id attribute.
        current_id (str): id of the user making the request 
    ---------------------------------------------------------
    Returns:
        InvalidRequest | SpecialtyDeleteRequest: Return an SpecialtyDeleteRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()
   
    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not specialty.id:
        invalid_request.add_error("specialty_id", "specialty is necessary")

    if invalid_request.has_error():
        return invalid_request

    return SpecialtyDeleteRequest(specialty, current_id)