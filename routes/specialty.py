# FastApi
from typing import List
from fastapi import APIRouter, Body, Path, Query, HTTPException, Depends


# Entities
from backend.entities.specialty import Specialty

# Auth
from auth.jwt import JWTHandler

# Requests
from backend.requests.specialty.specialty_create_request import build_specialty_create_request
from backend.requests.specialty.specialty_delete_request import build_specialty_delete_request
from backend.requests.specialty.specialty_find_request import build_specialty_find_request
from backend.requests.specialty.specialty_update_request import build_specialty_update_request

# UseCases
from backend.useCases.specialty.specialty_create_use_case import specialty_create_use_case
from backend.useCases.specialty.specialty_delete_use_case import specialty_delete_use_case
from backend.useCases.specialty.specialty_find_use_case import specialty_find_use_case
from backend.useCases.specialty.specialty_update_use_case import specialty_update_use_case

# Schemas
from schemas.specialty import SpecialtyIn, SpecialtyOut

# Repository
from backend.repositories import specialtyRepo

specialty = APIRouter(prefix='/specialties', tags=["Specialties"])
jwt_handler = JWTHandler()


@specialty.post('/', response_model=SpecialtyOut)
def create_specialty(specialty_in: SpecialtyIn = Body(...), current_id=Depends(jwt_handler.auth_wrapper)):
    specialty = Specialty.from_dict(specialty_in.dict())
    request_object = build_specialty_create_request(
        specialty=specialty, current_id=current_id)
    response = specialty_create_use_case(
        repo=specialtyRepo, request=request_object)

    if response:
        return response.value

    raise HTTPException(response.code, response.message)


@specialty.get('/', response_model=List[SpecialtyOut] | SpecialtyOut)
def find_specialty(id: str = Query(default=None), title: str = Query(default=None)):

    filters = {}
    filters["id"] = id
    filters["title"] = title
    filters = {key: value for (
        key, value) in filters.items() if value is not None}

    request_object = build_specialty_find_request(filters=filters)
    response = specialty_find_use_case(
        repo=specialtyRepo, request=request_object)

    if response:
        return response.value
    raise HTTPException(response.code, response.message)


@specialty.put('/{id_specialty}', response_model=SpecialtyOut)
def update_speciality(specialty_in: SpecialtyIn = Body(...), id_specialty: str = Path(...), current_id=Depends(jwt_handler.auth_wrapper)):
    specialty = Specialty.from_dict(specialty_in.dict())
    specialty.id = id_specialty
    request_object = build_specialty_update_request(specialty,current_id)
    response = specialty_update_use_case(
        repo=specialtyRepo, request=request_object)

    if response:
        return response.value
    raise HTTPException(response.code, response.message)

@specialty.delete('/{id_specialty}', response_model=SpecialtyOut)
def update_speciality( id_specialty: str = Path(...), current_id=Depends(jwt_handler.auth_wrapper)):
    specialty = Specialty(id=id_specialty)

    request_object = build_specialty_delete_request(specialty,current_id)
    response = specialty_delete_use_case(
        repo=specialtyRepo, request=request_object)

    if response:
        return response.value
    raise HTTPException(response.code, response.message)
