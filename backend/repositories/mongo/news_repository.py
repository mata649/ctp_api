from string import printable
from typing import List
from bson import ObjectId
from backend.repositories.mongo.mongo_repo import MongoRepo
from backend.entities.news import News
from pymongo import ReturnDocument
import re


class NewsRepository(MongoRepo):

    def _create_news_entity(self, news) -> News:
        news["id"] = str(news["_id"])
        del news["_id"]
        return News.from_dict(news)

    def _create_news_list_entity(self, news_list) -> List[News]:
        news_list = [self._create_news_entity(
            news) for news in news_list]
        return news_list

    def create_news(self, news: News):
        inserted_id = self.db.news.insert_one(
            {"title": news.title,
                "text": news.text,
                "published": news.published,
                "enable": news.enable,
             }
        ).inserted_id
        news.id = str(inserted_id)
        return news

    def find_news(self, filters: dict = None) -> News | List[News]:
        if not filters:
            news_list = self.db.news.find({'enable': True})
            return self._create_news_list_entity(news_list)
        else:
            if "id" in filters:
                filters["_id"] = ObjectId(filters["id"])
                del filters["id"]
            if "title" in filters:
                filters["title"] = re.compile(
                    f'.*{filters["title"]}.*', re.IGNORECASE)

            news = self.db.news.find(
                {**filters, 'enable': True},)
            news = list(news)
            if len(news) == 1:
                return self._create_news_entity(news[0])
            else:
                return self._create_news_list_entity(news)
       

    def update_news(self, news: News) -> News:
        id_to_search = ObjectId(news.id)

        specialty_updated = self.db.news.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    "title": news.title,
                    "text": news.text,
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )

        return self._create_news_entity(specialty_updated)

    def delete_news(self, news: News) -> News:
        id_to_search = ObjectId(news.id)
        news_deleted = self.db.news.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    'enable': False
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )
        return self._create_news_entity(news_deleted)
