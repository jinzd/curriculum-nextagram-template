from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(index=True, unique=True, null=False)
    password = pw.CharField(null=False)
    email = pw.CharField(unique=True, null=False)
