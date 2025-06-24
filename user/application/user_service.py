from typing import Annotated
from ulid import ULID
from datetime import datetime
from fastapi import HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from utils.crypto import Crypto
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository

class UserService:
    @inject
    def __init__(
            self,
            user_repo: IUserRepository,
        ):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
            self, 
            name: str,
            student_id: str,
            department: str,
            phone_number: str,
            email: str, 
            password: str,
            study: str
            ):
        _user = None

        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e
            
        if _user:
            raise HTTPException(status_code=422)
        
        now = datetime.now()
        user = User(
            id=self.ulid.generate(),
            name=name,
            student_id=student_id,
            department=department,
            phone_number=phone_number,
            email=email,
            password=self.crypto.encrypt(password),
            study=study,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)

        return user
    
    def update_user(
        self,
        user_id: str,
        name: str | None = None,
        student_id: str | None = None,
        department: str | None = None,
        phone_number: str | None = None,
        password: str | None = None,
        study: str | None = None,
    ):
        user = self.user_repo.find_by_id(user_id)

        if name:
            user.name = name
        if student_id:
            user.student_id = student_id
        if department:
            user.department = department
        if phone_number:
            user.phone_number = phone_number
        if password:
            user.password = self.crypto.encrypt(password)
        if study:
            user.study = study
        user.updated_at = datetime.now()

        self.user_repo.update(user)

        return user
