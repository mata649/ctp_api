# FastApi
from typing import List
from urllib import response
from fastapi import APIRouter, Body, Path, Query, HTTPException, Depends

# Entities
from backend.entities.workshop import Workshop

# Requests
from backend.requests.workshop.workshop_create_request import build_workshop_create_request
from backend.requests.workshop.workshop_delete_request import build_workshop_delete_request
from backend.requests.workshop.workshop_find_request import build_workshop_find_request
from backend.requests.workshop.workshop_update_request import build_workshop_update_request

# UseCases
from backend.useCases.workshop.workshop_create_use_case import workshop_create_use_case
from backend.useCases.workshop.workshop_delete_use_case import workshop_delete_use_case
from backend.useCases.workshop.workshop_find_use_case import workshop_find_use_case
from backend.useCases.workshop.workshop_update_use_case import workshop_update_use_case

# Auth
from auth.jwt import JWTHandler

# Schemas
from schemas.workshop import WorkshopIn, WorkshopOut

# Repository
from backend.repositories import workshopRepo


workshop = APIRouter(prefix='/workshops', tags=["Workshops"])
jwt_handler = JWTHandler()


@workshop.post('/', response_model=WorkshopOut)
def create_workshop(workshop_in: WorkshopIn = Body(...), current_id=Depends(jwt_handler.auth_wrapper)):

    workshop = Workshop.from_dict(workshop_in.dict())

    request_object = build_workshop_create_request(workshop, current_id)
    response = workshop_create_use_case(
        repo=workshopRepo, request=request_object)
    if response:
        return response.value
    raise HTTPException(response.code, detail=response.message)


@workshop.put('/{id_workshop}', response_model=WorkshopOut)
def update_workshop(
        workshop_in: WorkshopIn = Body(...),
        id_workshop: str = Path(...),
        current_id=Depends(jwt_handler.auth_wrapper)):

    workshop = Workshop.from_dict(workshop_in.dict())
    workshop.id = id_workshop

    request_object = build_workshop_update_request(workshop, current_id)
    response = workshop_update_use_case(
        repo=workshopRepo, request=request_object)
    if response:
        return response.value
    raise HTTPException(response.code, detail=response.message)


@workshop.get('/', response_model=List[WorkshopOut] | WorkshopOut)
def find_workshop(id: str = Query(default=None), title: str = Query(default=None)):

    filters = {}
    filters["id"] = id
    filters["title"] = title
    filters = {key: value for (
        key, value) in filters.items() if value is not None}

    request_object = build_workshop_find_request(filters=filters)
    response = workshop_find_use_case(
        repo=workshopRepo, request=request_object)

    if response:
        return response.value
    raise HTTPException(response.code, response.message)


@workshop.delete('/{id_workshop}', response_model=WorkshopOut)
def delete_workshop(id_workshop: str = Path(...), current_id=Depends(jwt_handler.auth_wrapper)):
    workshop = Workshop(id=id_workshop)

    request_object = build_workshop_delete_request(workshop, current_id)
    response = workshop_delete_use_case(
        repo=workshopRepo, request=request_object)

    if response:
        return response.value
    raise HTTPException(response.code, response.message)
