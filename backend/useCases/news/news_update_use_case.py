import logging
# External Libs
from colorama import Fore
from backend.helpers.news_exists import news_exists
from backend.helpers.user_is_authorized import user_is_authorized
from backend.repositories.mongo.news_repository import NewsRepository
from backend.requests.news.news_update_request import NewsUpdateRequest
from backend.requests.request import InvalidRequest
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def news_update_use_case(repo: NewsRepository, request: NewsUpdateRequest | InvalidRequest) -> ResponseSuccess | ResponseFailure:
    """Updates a news in a database.
    ----------------------------------------------------------
    Updates a news in the database, the NewsUpdateRequest has the payload with the 
    news information.
    -------------------------------------------------------------
    Args:
        repo (NewsRepository): An instance of the NewsRepository class with the method to update the news in the DB. 
        request (NewsUpdateRequest): An instance of NewsUpdateRequest with the news information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the update of the news was
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")
 

        news = request.news
        if not news_exists(news.id, repo):
            return ResponseFailure(404, "News doesn't exists")

        news = repo.update_news(news)
        return ResponseSuccess(news)

    except Exception as err:
        logger.warning(Fore.RED+str(err))
        return ResponseFailure(code=500, message=err)