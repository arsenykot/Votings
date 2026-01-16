from django.db.models import *

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_banned = BooleanField(default=False, help_text="Specifies whether this user is banned and can not access the website.")

class Voting(Model):
    author = ForeignKey(User, on_delete=CASCADE, related_name='votings')
    name = CharField(max_length=48)
    description = CharField(max_length=512)
    options = JSONField(default=list)
    multichoice = BooleanField(default=False)
    date_created = DateTimeField(auto_now=True)
    date_closed = DateTimeField(null=True, blank=True)
    taken_down = BooleanField(default=False)

