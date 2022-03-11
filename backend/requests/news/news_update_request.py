from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.news import News


class NewsUpdateRequest(ValidRequest):
    def __init__(self, news: News, current_id: str) -> None:
        self.news = news
        self.current_id = current_id




def build_news_update_request(news: News, current_id: str) -> InvalidRequest | NewsUpdateRequest:
    """Validates a NewsUpdateRequest information.
    -----------------------------------------------------
    Validates that the news attributes meet the requirements of the request.
    -----------------------------------------------------
    Args:
        news (News): A News entity with the id, title and text attributes.
        current_id (str): id of the user making the request 
    ----------------------------------------------------- 
    Returns:
        InvalidRequest | NewsUpdateRequest: Return an NewsUpdateRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()

    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not news.title:
        invalid_request.add_error("title", "The title is necessary")
    
    if not news.text:
        invalid_request.add_error("text", "The text is necessary")

    if not news.id:
        invalid_request.add_error("id", "The id is necessary")

    if invalid_request.has_error():
        return invalid_request
   
    return NewsUpdateRequest(news, current_id)
