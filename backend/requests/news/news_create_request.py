from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.news import News


class NewsCreateRequest(ValidRequest):
    def __init__(self, news: News, current_id: str) -> None:
        self.news = news
        self.current_id = current_id




def build_news_create_request(news: News, current_id: str) -> InvalidRequest | NewsCreateRequest:
    """Validates a NewsCreateRequest information.
    -----------------------------------------------------
    Validates that the news attributes meet the requirements of the request.
    -----------------------------------------------------
    Args:
        news (News): A News entity with the title and text attributes.
        current_id (str): id of the user making the request 
    ----------------------------------------------------- 
    Returns:
        InvalidRequest | NewsCreateRequest: Return an NewsCreateRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()

    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not news.title.rstrip():
        invalid_request.add_error("title", "The title is necessary")
    
    if not news.text.rstrip():
        invalid_request.add_error("text", "The text is necessary")

    if invalid_request.has_error():
        return invalid_request
   
    return NewsCreateRequest(news, current_id)
