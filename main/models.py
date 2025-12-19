from django.db.models import *

# Create your models here.
class User(Model):
    username = CharField(max_length=24)
    password = CharField(max_length=32)
    token = CharField(max_length=32)
    is_admin = BooleanField(default=False)