from typing import Union, Dict, Any, NoReturn
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.refresh_token import RefreshToken
from app.schemas.refresh_token import RefreshTokenCreate, RefreshTokenUpdate
from app.db.session import session


class CRUDRefreshToken(CRUDBase[RefreshToken, RefreshTokenCreate, RefreshTokenUpdate]):
    def create(self, *, obj_in: RefreshTokenCreate) -> RefreshToken:
        db_obj = RefreshToken(
            obj_in.user_id,
            obj_in.jti,
            obj_in.token
        )

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj

    def update(
            self,
            *,
            db_obj: RefreshToken,
            obj_in: Union[RefreshTokenUpdate, Dict[str, Any]],
    ) -> RefreshToken:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db_obj=db_obj, obj_in=update_data)

    def get_by_user_id(self, *, user_id: int) -> RefreshToken:
        return session.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()

    def get_by_jti(self, *, jti: str) -> RefreshToken:
        return session.query(RefreshToken).filter(RefreshToken.jti == jti).first()

    def revoke(self, *, jti: str) -> NoReturn:
        db_obj = self.get_by_jti(jti=jti)
        self.update(db_obj=db_obj, obj_in={'revoked_at': datetime.now()})


refresh_token = CRUDRefreshToken(RefreshToken)
