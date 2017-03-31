from django.contrib import admin

from .models import Command, Response

admin.site.register(Command)
admin.site.register(Response)