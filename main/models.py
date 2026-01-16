from django.db.models import *

from django.contrib.auth.models import User

class Voting(Model):
    author = ForeignKey(User, on_delete=CASCADE, related_name='votings')
    name = CharField(max_length=48)
    description = CharField(max_length=512)
    option1 = CharField(max_length=48)
    option2 = CharField(max_length=48)
    date_created = DateTimeField(auto_now=True)
    date_closed = DateTimeField(null=True, blank=True)