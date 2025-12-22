from django.db.models import *

from django.contrib.auth.models import User

class Voting(Model):
    author = ForeignKey(User, on_delete=CASCADE, related_name='votings')
    option1 = CharField(max_length=64)
    option2 = CharField(max_length=64)