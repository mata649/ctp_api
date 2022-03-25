from backend.entities.workshop import Workshop
from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.specialty import Specialty


class WorkshopCreateRequest(ValidRequest):
    def __init__(self, workshop: Workshop, current_id: str) -> None:
        self.workshop = workshop
        self.current_id = current_id




def build_workshop_create_request(workshop: Workshop, current_id: str) -> InvalidRequest | WorkshopCreateRequest:
    """Validates a WorkshopCreateRequest information.
    -----------------------------------------------------
    Validates that the workshop attributes meet the requirements of the request.
    -----------------------------------------------------
    Args:
        workshop (Workshop): A Workshop entity with at least title, description and color attributes.
        current_id (str): id of the user making the request 
    ----------------------------------------------------- 
    Returns:
        InvalidRequest | WorkshopCreateRequest: Return an WorkshopCreateRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()

    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not workshop.title.rstrip():
        invalid_request.add_error("title", "The title is necessary")
    
    if not workshop.description.rstrip():
        invalid_request.add_error("description", "The description is necessary")
    
    if not workshop.color:
        invalid_request.add_error("color", "The color is necessary")
    
    if type(workshop.images) != list:
        invalid_request.add_error("images", "The images has to be a list")

    if invalid_request.has_error():
        return invalid_request
    
    return WorkshopCreateRequest(workshop, current_id)
