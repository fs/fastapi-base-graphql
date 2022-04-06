from typing import Dict, Any, Union, List

from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.user_activity import UserActivity, UserActivityTypeEnum
from app.schemas.user_activity import UserActivityCreate, UserActivityUpdate
from app.db.session import session


class CRUDUserActivity(CRUDBase[UserActivity, UserActivityCreate, UserActivityUpdate]):
    async def create(self, *, obj_in: UserActivityCreate) -> UserActivity:
        db_obj = UserActivity(
            user_id=obj_in.user_id,
            event=obj_in.event
        )

        await session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def update(
        self,
        *,
        db_obj: UserActivity,
        obj_in: Union[UserActivityUpdate, Dict[str, Any]],
    ) -> UserActivity:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def get_all_user_activities(self, *, user_id) -> List[UserActivity]:
        return await session.query(UserActivity).filter(UserActivity.user_id == user_id).all()

    async def get_all_activities_by_type(self, *, activity_type: UserActivityTypeEnum) -> List[UserActivity]:
        return await session.query(UserActivity).filter(UserActivity.event == activity_type).all()

    async def get_user_activities_by_type(self, user_id: int, activity_type: UserActivityTypeEnum) -> List[UserActivity]:
        return await session.query(UserActivity).filter(and_(UserActivity.user_id == user_id, UserActivity.event == activity_type)).all()


user_activity = CRUDUserActivity(UserActivity)
