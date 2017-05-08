"""
The Bestory Project
"""

from asyncpgsa import compile_query
from asyncpgsa.record import Record

# Patch for :class:`asyncpgsa.connection.SAConnection` method
async def fetchrow(self, query, *args, **kwargs):
    query, params = compile_query(query)
    result = await self._connection.fetchrow(query, *params, *args, **kwargs)
    return Record(result) if result is not None else None
