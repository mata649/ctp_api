from backend.repositories.mongo.mongo_repo import MongoRepo
from bson.objectid import ObjectId
from typing import List
from pymongo import ReturnDocument
from backend.entities.workshop import Workshop


class WorkshopRepository(MongoRepo):
    def _create_workshop_entity(self, workshop) -> Workshop:
        workshop["id"] = str(workshop["_id"])
        del workshop["_id"]
        return Workshop.from_dict(workshop)

    def _create_workshops_entity(self, workshops) -> List[Workshop]:
        workshops = [self._create_workshop_entity(
            workshop) for workshop in workshops]
        return workshops

    def create_workshop(self, workshop: Workshop):
        inserted_id = self.db.workshops.insert_one(
            {
                "title": workshop.title,
                "description": workshop.description,
                "images": workshop.images,
                "color": workshop.color,
                "enable": workshop.enable
            }
        ).inserted_id
        workshop.id = str(inserted_id)
        return workshop

    def find_workshop(self, filters: dict = None) -> Workshop | List[Workshop]:
        if not filters:
            workshops = self.db.workshops.find({'enable':True})
            return self._create_workshops_entity(workshops)
        else:
            if "id" in filters:
                filters["_id"] = ObjectId(filters["id"])
                del filters["id"]
            workshop = self.db.workshops.find_one(
                    {**filters, 'enable': True},)

            if workshop:
                return self._create_workshop_entity(workshop)
        return None

    def update_workshop(self, workshop: Workshop) -> Workshop:
        id_to_search = ObjectId(workshop.id)

        workshop_updated = self.db.workshops.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    "title": workshop.title,
                    "description": workshop.description,
                    "images": workshop.images,
                    "color": workshop.color,
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )

        return self._create_workshop_entity(workshop_updated)

    def delete_workshop(self, workshop: Workshop) -> Workshop:
        id_to_search = ObjectId(workshop.id)
        workshop_deleted = self.db.workshops.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    'enable': False
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )
        return self._create_workshop_entity(workshop_deleted)
