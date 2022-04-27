from datetime import datetime
from typing import Any, Dict, List, Union

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.session import session
from app.models.refresh_token import RefreshToken
from app.schemas.refresh_token import RefreshTokenCreate, RefreshTokenUpdate


class CRUDRefreshToken(CRUDBase[RefreshToken, RefreshTokenCreate, RefreshTokenUpdate]):
    """Database operations for refresh tokens."""

    async def create(self, *, obj_in: RefreshTokenCreate) -> RefreshToken:
        db_obj = RefreshToken(
            user_id=obj_in.user_id,
            jti=obj_in.jti,
            token=obj_in.token,
        )

        await session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            *,
            db_obj: RefreshToken,
            obj_in: Union[RefreshTokenUpdate, Dict[str, Any]],
    ) -> RefreshToken:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def get_all_by_user_id(self, *, user_id: int) -> List[RefreshToken]:
        return await session.query(RefreshToken).filter(RefreshToken.user_id == user_id).all()

    async def get_by_jti(self, *, jti: str) -> RefreshToken:
        return await session.query(RefreshToken).filter(RefreshToken.jti == jti).first()

    def filter_active_tokens_by_user_id(self, *, user_id: int) -> AsyncSession:
        active_lookup = and_(
            RefreshToken.revoked_at.is_(None),
            RefreshToken.user_id == user_id,
        )
        session.query(RefreshToken).filter(active_lookup)
        return session

    async def revoke(self, *, jti: str) -> None:
        db_obj = await self.get_by_jti(jti=jti)
        await self.update(db_obj=db_obj, obj_in={'revoked_at': datetime.now()})

    def revoke_all_for_user(self, *, user_id: int) -> None:
        active_user_tokens = self.filter_active_tokens_by_user_id(user_id=user_id)
        await active_user_tokens.update({'revoked_at': datetime.now()})
        await session.commit()


refresh_token = CRUDRefreshToken(RefreshToken)
