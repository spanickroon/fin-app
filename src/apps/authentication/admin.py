from django.contrib import admin
from django.contrib.auth.models import Group

from apps.authentication.models import UserProfile

admin.site.register(UserProfile)
admin.site.unregister(Group)