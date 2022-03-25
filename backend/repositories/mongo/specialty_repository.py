import re
from typing import List
from bson import ObjectId
from backend.repositories.mongo.mongo_repo import MongoRepo
from backend.entities.specialty import Specialty
from pymongo import ReturnDocument


class SpecialtyRepository(MongoRepo):

    def _create_specialty_entity(self, specialty) -> Specialty:
        specialty["id"] = str(specialty["_id"])
        del specialty["_id"]
        return Specialty.from_dict(specialty)

    def _create_specialties_entity(self, specialties) -> List[Specialty]:
        specialties = [self._create_specialty_entity(
            specialty) for specialty in specialties]
        return specialties

    def create_specialty(self, specialty: Specialty):
        inserted_id = self.db.specialties.insert_one(
            {
                "title": specialty.title,
                "description": specialty.description,
                "images": specialty.images,
                "recommended_skills": specialty.recommended_skills,
                "color": specialty.color,
                "enable": specialty.enable
            }
        ).inserted_id
        specialty.id = str(inserted_id)
        return specialty

    def find_specialty(self, filters: dict = None) -> Specialty | List[Specialty]:
        if not filters:
            specialties = self.db.specialties.find({'enable': True})
            return self._create_specialties_entity(specialties)
        else:
            if "id" in filters:
                filters["_id"] = ObjectId(filters["id"])
                del filters["id"]
            if "title" in filters:
                filters["title"] = re.compile(
                    f'.*{filters["title"]}.*', re.IGNORECASE)
            specialties = self.db.specialties.find(
                {**filters, 'enable': True},)
            specialties = list(specialties)
            if len(specialties) == 1:
                return self._create_specialty_entity(specialties[0])
            return self._create_specialties_entity(specialties)
        return None

    def update_specialty(self, specialty: Specialty) -> Specialty:
        id_to_search = ObjectId(specialty.id)

        specialty_updated = self.db.specialties.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    "title": specialty.title,
                    "description": specialty.description,
                    "images": specialty.images,
                    "recommended_skills": specialty.recommended_skills,
                    "color": specialty.color,
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )

        return self._create_specialty_entity(specialty_updated)

    def delete_specialty(self, specialty: Specialty) -> Specialty:
        id_to_search = ObjectId(specialty.id)
        specialty_deleted = self.db.specialties.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    'enable': False
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )
        return self._create_specialty_entity(specialty_deleted)
