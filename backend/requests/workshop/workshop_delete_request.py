from backend.entities.workshop import Workshop
from backend.requests.request import InvalidRequest, ValidRequest


class WorkshopDeleteRequest(ValidRequest):
    def __init__(self, workshop: Workshop, current_id: str) -> None:
        self.workshop = workshop
        self.current_id = current_id



def build_workshop_delete_request(workshop: Workshop, current_id: str) -> InvalidRequest | WorkshopDeleteRequest:
    """Validates a WorkshopDeleteRequest information.
    --------------------------------------------------------
    Validates that the current_id and workshop id attributes meet the requirements of the request.
  
    Args:
        workshop (Workshop): A Workshop entity with id attribute.
        current_id (str): id of the user making the request 
    ---------------------------------------------------------
    Returns:
        InvalidRequest | WorkshopDeleteRequest: Return an WorkshopDeleteRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()
   
    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not workshop.id:
        invalid_request.add_error("workshop_id", "workshop is necessary")

    if invalid_request.has_error():
        return invalid_request

    return WorkshopDeleteRequest(workshop, current_id)