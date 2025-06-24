from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from containers import Container

from user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str
    student_id: str
    department: str
    phone_number: str
    email: str
    password:str
    study: str

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    created_user = user_service.create_user(
            name=user.name,
            student_id=user.student_id,
            department=user.department,
            phone_number=user.phone_number,
            email=user.email,
            password=user.password,
            study=user.study,
    )
    return created_user

class UpdateUser(BaseModel):
        name: str | None = None
        student_id: str | None = None
        department: str | None = None
        phone_number: str | None = None
        password: str | None = None
        study: str | None = None

@router.put("/{user_id}")
@inject
def update_user(
    user_id: str,
    user: UpdateUser,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        student_id=user.student_id,
        department=user.department,
        phone_number=user.phone_number,
        password=user.password,
        study=user.study
    )

    return user