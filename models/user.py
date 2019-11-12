from flask import request, flash
from models.base_model import BaseModel
from peewee_validates import ModelValidator
import peewee as pw
import re


class User(BaseModel):
    username = pw.CharField(index=True, unique=True, null=False)
    password = pw.CharField(null=False)
    email = pw.CharField(unique=True, null=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username:
            self.errors.append('This username is already being used')
        else:
            if duplicate_email:
                self.errors.append(
                    'This email address is already being used')

            # duplicate_emails = User.get_or_none(User.email == self.email)
            # if duplicate_emails:
            #     self.errors.append('This email address is already being used')
