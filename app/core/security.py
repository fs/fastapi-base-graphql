import hashlib
from calendar import timegm
from datetime import datetime

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check password hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def generate_hash(string: str) -> str:
    """Generate unique hash by string."""
    get_hash = hashlib.new('MD5')  # noqa: S324
    get_hash.update(string.encode('utf-8'))
    return get_hash.hexdigest()


def generate_hash_for_jti(user_id: int, created_at: datetime) -> str:
    """Generate hash with options for unique."""
    timestamp = timegm(created_at.utctimetuple())
    key = f'{user_id}-{timestamp}'
    return generate_hash(key)
