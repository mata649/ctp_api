import logging
# External Libs
from colorama import Fore
from backend.helpers.news_exists import news_exists
from backend.helpers.user_is_authorized import user_is_authorized


from backend.repositories.mongo.news_repository import NewsRepository
from backend.requests.news.news_delete_request import NewsDeleteRequest


logger = logging.getLogger(__name__)

from backend.response import (
    ResponseFailure,
    ResponseSuccess,
    build_response_from_invalid_request
)


def news_delete_use_case(repo: NewsRepository, request: NewsDeleteRequest) -> ResponseSuccess | ResponseFailure:
    """Deletes a news in a database.
    ----------------------------------------------------------
    Deletes a news in the database, the NewsDeleteRequest has the payload with the 
    news information.
    -------------------------------------------------------------
    Args:
        repo (NewsRepository): An instance of the NewsRepository class with the method to delete the news in the DB. 
        request (NewsDeleteRequest): An instance of NewsDeleteRequest with the news information.

    Returns:
        ResponseFailure | ResponseSuccess: Return a ResponseSuccess if the elimination of the news was 
        successful, else return a ResponseFailure
    """
    if not request:
        return build_response_from_invalid_request(request)

    try:

        if not user_is_authorized(id=request.current_id):
            return ResponseFailure(401, "Unauthorized")

        if not news_exists(id=request.news.id, repo=repo):
            return ResponseFailure(404, "News doesn't exists")

        news = repo.delete_news(request.news)

        return ResponseSuccess(news)

    except Exception as err:
        logger.warning(Fore.RED + str(err))
        return ResponseFailure(code=500, message=err)
