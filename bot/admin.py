from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Command, Response, Unit, Session, Activity

class MyAdmin(TreeAdmin):
    form = movenodeform_factory(Unit)

admin.site.register(Unit, MyAdmin)

admin.site.register(Command)
admin.site.register(Response)
# admin.site.register(Unit)
# admin.site.register(Session)
# admin.site.register(Activity)