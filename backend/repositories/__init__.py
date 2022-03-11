from backend.repositories.mongo.news_repository import NewsRepository
from backend.repositories.mongo.specialty_repository import SpecialtyRepository
from backend.repositories.mongo.user_repository import UserRepository
from backend.repositories.mongo.workshop_repository import WorkshopRepository

userRepo = UserRepository()
specialtyRepo = SpecialtyRepository()
workshopRepo = WorkshopRepository()
newsRepo = NewsRepository()
