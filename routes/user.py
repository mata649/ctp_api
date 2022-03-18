# FastApi
from typing import List
from fastapi import APIRouter, Body, Path, Query, HTTPException, Depends

# Auth
from auth.jwt import JWTHandler

# Helpers
from backend.helpers.user_is_authorized import user_is_authorized

# Requests
from backend.requests.user.user_create_request import build_user_create_request
from backend.requests.user.user_delete_request import build_user_delete_request
from backend.requests.user.user_find_request import build_user_find_request
from backend.requests.user.user_login_request import build_user_login_request
from backend.requests.user.user_update_request import build_user_update_request
from backend.requests.user.user_change_password_request import build_user_change_password_request

# useCases
from backend.useCases.user.user_change_password_use_case import user_change_password_use_case
from backend.useCases.user.user_create_use_case import user_create_use_case
from backend.useCases.user.user_delete_use_case import user_delete_use_case
from backend.useCases.user.user_find_use_case import user_find_use_case
from backend.useCases.user.user_login_use_case import user_login_use_case
from backend.useCases.user.user_update_use_case import user_update_use_case

# Entities
from backend.entities.user import User

# Schemas
from schemas.user import UserChangePasswordIn, UserChangePasswordOut, UserIn, UserLoginIn, UserLoginOut, UserOut, UserUpdateIn, UserUpdateOut

# Repository
from backend.repositories import userRepo

user = APIRouter(prefix='/users', tags=["Users"])
jwt_handler = JWTHandler()


@user.post('/login', response_model=UserLoginOut)
def login_user(user_in: UserLoginIn = Body(...)):

    user = User.from_dict(user_in.dict())

    request_object = build_user_login_request(user=user)
    response = user_login_use_case(userRepo, request_object)

    if response:
        user_dict = response.value.to_dict()

        user_dict["jwt"] = jwt_handler.encode_token(user_dict["id"])
        return user_dict

    raise HTTPException(response.code, detail=response.message)


@user.post('/', status_code=201, response_model=UserOut)
def create_user(
        user_in: UserIn = Body(...),
        current_id=Depends(jwt_handler.auth_wrapper)):

    user: User = User.from_dict(user_in.dict())
    request_object = build_user_create_request(user, current_id)

    response = user_create_use_case(repo=userRepo, request=request_object)
    if response:
        return response.value
    raise HTTPException(response.code, detail=response.message)


@user.put('/{user_id}', status_code=200, response_model=UserUpdateOut)
def update_user(
        user_in: UserUpdateIn = Body(...,),
        user_id: str = Path(...),
        current_id=Depends(jwt_handler.auth_wrapper)):

    user: User = User.from_dict(user_in.dict())
    user.id = user_id

    request_object = build_user_update_request(user, current_id)
    response = user_update_use_case(repo=userRepo, request=request_object)
    if response:
        user = response.value
        return user

    raise HTTPException(response.code, detail=response.message)


@user.put('/change_password/{user_id}', status_code=200, response_model=UserChangePasswordOut)
def change_password_user(
        user_in: UserChangePasswordIn = Body(...,),
        user_id: str = Path(...),
        current_id=Depends(jwt_handler.auth_wrapper)):

    user: User = User.from_dict(user_in.dict())
    user.id = user_id

    request_object = build_user_change_password_request(user, current_id)
    response = user_change_password_use_case(
        repo=userRepo, request=request_object)
    if response:
        return response.value
    raise HTTPException(response.code, detail=response.message)


@user.get('/', response_model=List[UserOut] | UserOut)
def get_users(
        email: str = Query(default=None),
        id: str = Query(default=None), current_id=Depends(jwt_handler.auth_wrapper)):
    filters = {}
    filters["email"] = email
    filters["id"] = id
    filters = {key: value for (
        key, value) in filters.items() if value is not None}

    if not user_is_authorized(id=current_id):
        raise HTTPException(401, "Unauthorized")

    request_object = build_user_find_request(filters)
    response = user_find_use_case(userRepo, request_object)
    if response:
        return response.value
    raise HTTPException(response.code, detail=response.message)


@user.get('/user_logged_info', response_model=UserOut)
def get_user_logged_info(current_id=Depends(jwt_handler.auth_wrapper)):
    request_object = build_user_find_request({'id': current_id})
    response = user_find_use_case(userRepo, request_object)
    if response:
        return response.value
    raise HTTPException(response.code, detail=response.message)


@user.delete('/{user_id}', response_model=UserOut)
def delete_user(user_id: str = Path(...), current_id=Depends(jwt_handler.auth_wrapper)):
    user = User(id=user_id)
    request_object = build_user_delete_request(user, current_id)
    response = user_delete_use_case(userRepo, request_object)
    if response:
        return response.value
    raise HTTPException(response.code, detail=response.message)
