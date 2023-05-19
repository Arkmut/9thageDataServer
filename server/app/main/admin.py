from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username" field
    fields = ["username"]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# data models


admin.site.register(ArmyBook)

