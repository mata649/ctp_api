from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.specialty import Specialty


class SpecialtyUpdateRequest(ValidRequest):
    def __init__(self, specialty: Specialty, current_id: str) -> None:
        self.specialty = specialty
        self.current_id = current_id




def build_specialty_update_request(specialty: Specialty, current_id: str) -> InvalidRequest | SpecialtyUpdateRequest:
    """Validates a SpecialtyUpdateRequest information.
    -----------------------------------------------------
    Validates that the specialty attributes meet the requirements of the request.
    -----------------------------------------------------
    Args:
        specialty (Specialty): A Specialty entity with at least title, description and color attributes.
        current_id (str): id of the user making the request 
    ----------------------------------------------------- 
    Returns:
        InvalidRequest | SpecialtyUpdateRequest: Return an SpecialtyUpdateRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()
  
    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not specialty.id:
        invalid_request.add_error("id", "id is necessary")

    if not specialty.title:
        invalid_request.add_error("title", "The title is necessary")
    
    if not specialty.description:
        invalid_request.add_error("description", "The description is necessary")
    
    if not specialty.color:
        invalid_request.add_error("color", "The color is necessary")
    
    if type(specialty.images) != list:
        invalid_request.add_error("images", "The images has to be a list")
    
    if type(specialty.recommended_skills) != list:
        invalid_request.add_error("recommended_skills", "The recomended_skills has to be a list")
    
    if invalid_request.has_error():
        return invalid_request

    return SpecialtyUpdateRequest(specialty, current_id)
