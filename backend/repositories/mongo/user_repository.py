from backend.repositories.mongo.mongo_repo import MongoRepo
from bson.objectid import ObjectId
from backend.entities.user import User
from typing import List
from pymongo import ReturnDocument


class UserRepository(MongoRepo):
    def _create_user_entity(self, user) -> User:
        user["id"] = str(user["_id"])
        del user["_id"]
        return User.from_dict(user)

    def _create_users_entity(self, users) -> List[User]:
        users = [self._create_user_entity(user) for user in users]
        return users

    def find_user(self, filters: dict = None) -> User | List[User]:

        if not filters:
            users = self.db.users.find({'role': {'$nin': ['SUPERADMIN']}, 'enable': True})
            return self._create_users_entity(users)
        else:
            if "id" in filters:
                filters["_id"] = ObjectId(filters["id"])
                del filters["id"]
            user = self.db.users.find_one({**filters, 'enable': True},)
            
            if user:
                return self._create_user_entity(user)
        return None

    def create_user(self, user: User) -> User:
        inserted_id = self.db.users.insert_one({
            'full_name': user.full_name,
            'email': user.email,
            'password': user.password,
            'enable': user.enable,
            'role': user.role
        }).inserted_id
        user.id = str(inserted_id)
        return user

    def update_user(self, user: User) -> User:
        id_to_search = ObjectId(user.id)
        user_updated = self.db.users.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    "full_name": user.full_name,
                    "role": user.role,
                    "email": user.email
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )

        return self._create_user_entity(user_updated)

    def change_user_password(self, user: User) -> User:
        id_to_search = ObjectId(user.id)
        user_updated = self.db.users.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    'password': user.password
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )

        return self._create_user_entity(user_updated)

    def delete_user(self, user: User) -> User:
        id_to_search = ObjectId(user.id)
        user_deleted = self.db.users.find_one_and_update(
            filter={'_id': id_to_search},
            update={
                '$set': {
                    'enable': False
                }
            }, upsert=False, return_document=ReturnDocument.AFTER
        )
        return self._create_user_entity(user_deleted)
