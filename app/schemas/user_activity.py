from datetime import datetime

from pydantic import BaseModel
from typing import Optional
from app.models.user_activity import UserActivityTypeEnum


class UserActivityBase(BaseModel):
    event: Optional[UserActivityTypeEnum] = None
    user_id: Optional[int] = None

    class Config:
        use_enum_values = True


class UserActivityCreate(UserActivityBase):
    event: UserActivityTypeEnum
    user_id: int


class UserActivityUpdate(UserActivityBase):
    event: UserActivityTypeEnum
    user_id: int


class UserActivityInDBBase(UserActivityBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserActivity(UserActivityInDBBase):
    pass


class UserActivityInDB(UserActivityInDBBase):
    created_at: datetime
