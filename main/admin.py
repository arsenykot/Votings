from django.contrib import admin
import django.contrib.auth.models
from main.models import *

@admin.action(description="Ban selected users")
def ban_user(modeladmin, request, queryset):
    queryset.update(is_banned = True, is_staff = False, is_superuser = False)

class UserAdmin(admin.ModelAdmin):
    list_display = ["username"]
    ordering = ["username"]
    actions = [ban_user]


@admin.action(description="Take selected votings down")
def remove_votings_soft(modeladmin, request, queryset):
    queryset.update(taken_down = True)

@admin.action(description="Take selected votings down and ban the authors")
def remove_votings_hard(modeladmin, request, queryset):
    queryset.update(taken_down = True)
    for entry in queryset:
        entry.author.is_banned = True

class VotingAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    ordering = ["id"]
    actions = [remove_votings_soft, remove_votings_hard]

admin.site.unregister(django.contrib.auth.models.Group)
admin.site.register(User, UserAdmin)

admin.site.register(Voting, VotingAdmin)