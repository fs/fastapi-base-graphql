from app.crud import crud_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException
from app.schemas.user import UserCreate
from app.graphql.types import users
from app.api.deps import get_db
import strawberry
from app.graphql.inputs.users import CreateUser
from app.db.session import session


def create_user(input: CreateUser) -> users.User:
    """Create user mutation test resolver."""
    user = crud_user.user.get_by_email(email=input.email)
    if user:
        raise ValueError('User already created')
    user = crud_user.user.create(obj_in=user)
    return user


@strawberry.type
class Mutation:
    """User mutation fields."""

    create_user = strawberry.field(resolver=create_user)
