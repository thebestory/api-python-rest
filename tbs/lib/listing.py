"""
The Bestory Project
"""

from enum import IntEnum
from typing import Optional, Tuple, Union


class Direction(IntEnum):
    BEFORE = -1
    AROUND = 0
    AFTER = 1


class Listing:
    """
    Listing class.

    Methods for working with listings.
    IDs of things can be provided in 10 base as int (0-9 digits,
    internal ids) or in 36 base as str (0-9 digits + a-z characters,
    public ids).
    """

    def __init__(self, min_limit: int, max_limit: int, default_limit: int):
        self._min_limit = min_limit
        self._max_limit = max_limit

        if self.validate_limit(default_limit) != default_limit:
            raise ValueError("Your default limit value does not comply with "
                             "the min and max value requirements.")

        self._default_limit = default_limit

    def validate_limit(self, limit: Optional[Union[int, str]] = None) -> int:
        """
        Returns limit value, which comply with the min and max value
        requirements.
        """
        if limit is None:
            return self._default_limit

        if isinstance(limit, str):
            limit = int(limit)

        return max(self._min_limit, min(self._max_limit, limit))

    @staticmethod
    def validate_id(id: Union[int, str]) -> Optional[int]:
        """
        Returns validated ID.
        """
        if isinstance(id, str):
            limit = int(id)

        if 0 <= id:
            return id

        return None

    def validate(self,
                 before: Optional[Union[int, str]]=None,
                 after: Optional[Union[int, str]]=None,
                 limit: Optional[Union[int, str]]=None
                 ) -> Tuple[Optional[int], int, Direction]:
        """
        Returns a ID of thing, from  which to search, and the correct
        value of limit. If neither of `before` and `after` is
        specified, returns None as ID of thing and `after`, that means
        to search from start of the list of things.
        """
        limit = self.validate_limit(limit)

        if before and after:
            raise ValueError("Only one of `before` and `after` arguments must "
                             "be specified")

        if before is not None:
            return self.validate_id(before), limit, Direction.BEFORE

        if after is not None:
            return self.validate_id(after), limit, Direction.AFTER

        return None, limit, Direction.AFTER
