from django.db.models import *

import time

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_banned = BooleanField(default=False, help_text="Specifies whether this user is banned and can not access the website.")
    preferred_theme = CharField(default="dark")

class Voting(Model):
    author = ForeignKey(User, on_delete=CASCADE, related_name='votings')
    name = CharField(max_length=48)
    description = CharField(max_length=512)
    options = JSONField(default=list)
    multichoice = BooleanField(default=False)
    date_created = DateTimeField(auto_now=True)
    date_closed = DateTimeField(null=True, blank=True)
    taken_down = BooleanField(default=False)
    closed = BooleanField(default=False)
    
    @classmethod
    def from_db(cls, db, field_names, values):
        voting = super().from_db(db, field_names, values)
        voting.check_closing_time()
        return voting

    def check_closing_time(self):
        if self.date_closed and self.date_closed.timestamp() < time.time():
            self.closed = True
            self.save()
        print("closing time:", self.date_closed)

class Vote(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    voting = ForeignKey(Voting, on_delete=CASCADE)
    choice = JSONField(default=list)
