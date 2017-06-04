"""
The Bestory Project
"""

from jose import jwt
from jose.exceptions import JWTError

from tbs import db
from tbs.config import jose as config
from tbs.lib import exceptions
from tbs.lib import stores


async def create(user):
    """Create a new JWT for session of the user."""
    # TODO: Save session to the DB.
    return {
        "user": user,
        "jwt": jwt.encode(
            {
                "user": user["id"],
                "iss": config.ISSUER
            },
            config.SECRET,
            config.ALGORITHM
        )
    }


async def validate(token: str):
    """Validate a JWT."""
    try:
        # TODO: Check session in the DB.

        return "user" in jwt.decode(token, config.SECRET, config.ALGORITHM)
    except JWTError:
        return False


async def decode(token: str):
    """Decode a JWT into session and fetch user from DB."""
    try:
        payload = jwt.decode(token, config.SECRET, config.ALGORITHM)

        async with db.pool.acquire() as conn:
            try:
                user = await stores.user.get(conn, payload["user"])

                return {
                    "user": user,
                    "jwt": token
                }
            except exceptions.NotFoundError:
                return None
    except JWTError:
        return None


async def revoke(token: str):
    """Delete session of the user and invalidate a JWT."""
    # TODO: Remove session from the DB.
    return True


async def middleware(request):
    """Decodes a session from the request."""
    request["session"] = None
    authorization = request.headers.get('Authorization', None)

    if authorization is None:
        return

    token = authorization.split()[-1]

    if await validate(token):
        request["session"] = await decode(token)
