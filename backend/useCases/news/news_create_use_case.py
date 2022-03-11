from datetime import datetime

import logging
# External Libs
from colorama import Fore
from backend.helpers.user_is_authorized import user_is_authorized
from backend.repositories.mongo.news_repository import NewsRepository
from backend.requests.news.news_create_request import NewsCreateRequest
from backend.requests.request import InvalidRequest

logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def news_create_use_case(repo: NewsRepository, request: NewsCreateRequest | InvalidRequest) -> ResponseSuccess | ResponseFailure:
    """Creates a news in a database.
    ----------------------------------------------------------
    Creates a news in the database, the NewsCreateRequest has the payload with the 
    news information.
    -------------------------------------------------------------
    Args:
        repo (NewsRepository): An instance of the NewsRepository class with the method to register the news in the DB. 
        request (NewsCreateRequest): An instance of NewsCreateRequest with the news information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the register of the news was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:
        
        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")
        
        news = request.news
        news.published = datetime.now()
        
        news = repo.create_news(news)

        return ResponseSuccess(news)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
