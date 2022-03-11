from backend.repositories.mongo.news_repository import NewsRepository
from backend.requests.news.news_find_request import build_news_find_request
from backend.useCases.news.news_find_use_case import news_find_use_case

def news_exists(id: str, repo: NewsRepository) -> bool:
    """Checks if a news exists in the database, based in the news id

    Args:
        id (str): The id of the news.
        repo (NewsRepository): An instance of a NewsRepository object.

    Returns:
        bool: Returns True if the news exists, else return False
    """
    
    req_news_by_id = build_news_find_request(
            {"id": id})
    response = news_find_use_case(repo, req_news_by_id)

    if response and response.value.enable:
        return True
    return False