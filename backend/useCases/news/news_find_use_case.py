import logging
from colorama import Fore
from backend.repositories.mongo.news_repository import NewsRepository
from backend.requests.news.news_find_request import NewsFindRequest


from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def news_find_use_case(repo: NewsRepository, request: NewsFindRequest) -> ResponseFailure | ResponseSuccess:
    """ Get news from the database.
    -------------------------------------------
    Get one news o more from the database based in the filters of the 
    NewsFindRequest payload. If the NewsFindRequest doesn't has
    a payload, return all the news in the database.
    Args:
        repo (NewsRepository): An instance of the NewsRepository class with the method to find the news in the DB 
        request (NewsFindRequest): An instance of NewsFindRequest with the filters of the query.

    Returns:
       ResponseFailure | ResponseSuccess : Return a ResponseSuccess if a news was found successfully, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:

        news = repo.find_news(request.filters)
        
        if not news:
            return ResponseFailure(404, "News doesn't exists")

        return ResponseSuccess(news)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message="Server Error")
