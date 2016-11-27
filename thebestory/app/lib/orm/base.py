"""
The Bestory Project
"""


"""
class BaseModel(orm.Model):
    class Meta:
        db = ...

class SomeModel(BaseModel):
    class Schema:
        id = IntegerField(primary_key=True)

    class Meta(BaseModel.Meta):
        tablename = ...
"""

"""
class BaseMeta(orm.Meta):
    db = ...

class SomeModel:
    class Schema:
        id = IntegerField(primary_key=True)

    class Meta(BaseMeta):
        tablename = ...
"""

