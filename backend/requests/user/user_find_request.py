from typing import Mapping
from backend.requests.request import InvalidRequest, ValidRequest


class UserFindRequest(ValidRequest):
    def __init__(self, filters):
        self.filters = filters


def build_user_find_request(filters: dict = None) -> UserFindRequest | InvalidRequest:
    """Validates a UserFindRequest filters.
    -----------------------------------------------------
    Validates that the filters meet the requirements of the request.
    The accepted filters are id, full_name and email.
-----------------------------------    ------------------ 
    Args:
        filters (dict, optioanl): A dict with the filter method. Defaults None. 
    ----------------------------------------------------- 
    Returns:
        InvalidRequest | UserFindRequest: Return an UserFindRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    
    invalid_request = InvalidRequest()
    accepted_filters = ["full_name", "email", "id"]

    if filters:
        if not isinstance(filters, Mapping):
            invalid_request.add_error("filters", "Is not iterable")
            return invalid_request

        for key, value in filters.items():
            if key not in accepted_filters:
                invalid_request.add_error(
                    "filters", "Key {} cannot be used".format(key)
                )
   

    if invalid_request.has_error():
        return invalid_request

    return UserFindRequest(filters)