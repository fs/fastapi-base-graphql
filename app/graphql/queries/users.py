from app.crud import crud_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException
from app.schemas.user import UserCreate
from app.graphql.types import users
from app.api.deps import get_db
import strawberry
from typing import List
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload, lazyload
from app.models.user import User
from app.db.session import session


def get_users() -> List[users.User]:
    """Get all users."""
    return session.query(User).all()


@strawberry.type
class Query:
    """User query fields."""

    users = strawberry.field(resolver=get_users)
