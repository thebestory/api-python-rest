"""
The Bestory
thebestory.models
"""

from sqlalchemy.ext.declarative import declarative_base


class BaseModel:
    pass

Model = declarative_base(cls=BaseModel)
