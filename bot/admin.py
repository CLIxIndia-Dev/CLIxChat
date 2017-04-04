from django.contrib import admin

from .models import Command, Response, Unit, Session, Activity

admin.site.register(Command)
admin.site.register(Response)
admin.site.register(Unit)
admin.site.register(Session)
admin.site.register(Activity)