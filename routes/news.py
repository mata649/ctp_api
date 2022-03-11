# FastApi
from pydoc import resolve
from typing import List
from urllib import request, response
from fastapi import APIRouter, Body, Path, Query, HTTPException, Depends

# Entities
from backend.entities.news import News

# Auth
from auth.jwt import JWTHandler

# Requests
from backend.requests.news.news_create_request import build_news_create_request
from backend.requests.news.news_find_request import build_news_find_request
from backend.requests.news.news_update_request import build_news_update_request

# UseCases
from backend.useCases.news.news_create_use_case import news_create_use_case
from backend.useCases.news.news_find_use_case import news_find_use_case
from backend.useCases.news.news_update_use_case import news_update_use_case

# Schemas
from schemas.news import NewsIn, NewsOut

# Repository

from backend.repositories import newsRepo

news = APIRouter(prefix='/news', tags=["News"])
jwt_handler = JWTHandler()


@news.post('/', response_model=NewsOut)
def create_news(news_in: NewsIn = Body(...), current_id=Depends(jwt_handler.auth_wrapper)):
    news = News.from_dict(news_in.dict())
    request_object = build_news_create_request(news, current_id)
    response = news_create_use_case(newsRepo, request_object)
    if response:
        return response.value

    raise HTTPException(response.code, response.message)


@news.put('/{news_id}', response_model=NewsOut)
def update_news(news_in: NewsIn = Body(...), news_id: str = Path(...), current_id=Depends(jwt_handler.auth_wrapper)):
    news = News.from_dict(news_in.dict())
    news.id = news_id
    request_object = build_news_update_request(news, current_id)
    response = news_update_use_case(newsRepo, request_object)
    if response:
        return response.value

    raise HTTPException(response.code, response.message)


@news.get('/', response_model=NewsOut | List[NewsOut])
def find_news(id: str = Query(default=None), title: str = Query(default=None)):
    filters = {}
    filters["id"] = id
    filters["title"] = title
    filters = {key: value for (
        key, value) in filters.items() if value is not None}

    request_object = build_news_find_request(filters=filters)
    response = news_find_use_case(newsRepo, request_object)
    if response:
        return response.value

    raise HTTPException(response.code, response.message)


@news.delete('/{news_id}', response_model=NewsOut)
def find_news(news_id: str = Path(...), current_id=Depends(jwt_handler.auth_wrapper)):
    news = News(id=news_id)
    request_object = build_news_find_request(filters=filters)
    response = news_find_use_case(newsRepo, request_object)
    if response:
        return response.value

    raise HTTPException(response.code, response.message)
