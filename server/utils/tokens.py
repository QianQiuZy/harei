import os
import time
import uuid
from typing import Optional

import redis


class TokenStore:
    def __init__(self) -> None:
        self._memory = {}
        self._redis = None
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            self._redis = redis.Redis.from_url(redis_url, decode_responses=True)

    def create_token(self, ttl_seconds: int) -> str:
        token = uuid.uuid4().hex
        if self._redis:
            self._redis.setex(token, ttl_seconds, "1")
        else:
            self._memory[token] = time.time() + ttl_seconds
        return token

    def validate(self, token: str) -> bool:
        if not token:
            return False
        if self._redis:
            return bool(self._redis.get(token))
        expires = self._memory.get(token)
        if not expires:
            return False
        if expires < time.time():
            self._memory.pop(token, None)
            return False
        return True


TOKEN_STORE = TokenStore()
