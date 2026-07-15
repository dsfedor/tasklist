from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models 
from database import get_db
from dependencies import get_current_user
from repositories.users import UserRepository
from schemas import TokenOut, UserCreate, UserOut
from services.auth import AuthService
 
router = APIRouter(prefix="/auth", tags=["auth"])
 
 
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
 
 
def get_auth_service(
    repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repo)
 
 
@router.post("/register", response_model=UserOut, status_code=201)
def register(
    payload: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    return service.register(payload)
 
 
@router.post("/login", response_model=TokenOut)
def login(
    payload: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    return service.authenticate(payload.email, payload.password)
 

@router.get("/users", response_model=list[UserOut])
def get_users(
    limit: int = 10,
    service: AuthService = Depends(get_auth_service),
    current_user: models.User = Depends(get_current_user),
):
    return service.list(current_user.id, limit=limit) 