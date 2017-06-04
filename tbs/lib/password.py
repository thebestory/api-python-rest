"""
The Bestory Project
"""

import passlib.context

from tbs.config import passlib as config


__crypt_context = passlib.context.CryptContext(schemes=config.SCHEMES)


def hash(raw: str) -> str:
    """Hash the password with a randomly generated salt."""
    return __crypt_context.hash(raw)


def verify(raw: str, crypted: str) -> bool:
    """Match a raw and crypted password."""
    try:
        return __crypt_context.verify(raw, crypted)
    except ValueError:
        return False


def identify(crypted: str):
    """Identify which algorithm the hash belongs to."""
    return __crypt_context.identify(crypted)
