from backend.requests.request import InvalidRequest, ValidRequest
from backend.entities.news import News


class NewsDeleteRequest(ValidRequest):
    def __init__(self, news: News, current_id: str) -> None:
        self.news = news
        self.current_id = current_id



def build_news_delete_request(news: News, current_id: str) -> InvalidRequest | NewsDeleteRequest:
    """Validates a NewsDeleteRequest information.
    --------------------------------------------------------
    Validates that the current_id and news id attributes meet the requirements of the request.
  
    Args:
        news (News): A News entity with id attribute.
        current_id (str): id of the user making the request 
    ---------------------------------------------------------
    Returns:
        InvalidRequest | NewsDeleteRequest: Return an NewsDeleteRequest with a payload
        if the attributes meet the requeriments, if one attribute doens't meet the requeriments
        return an InvalidRequest. 
    """
    invalid_request = InvalidRequest()
   
    if not current_id:
        invalid_request.add_error("current_id", "current_id is necessary")

    if not news.id:
        invalid_request.add_error("news_id", "news is necessary")

    if invalid_request.has_error():
        return invalid_request

    return NewsDeleteRequest(news, current_id)