from django.contrib import admin
from django.contrib.auth.models import Group

from app import models


admin.site.register(models.Person)
admin.site.register(models.Day)
admin.site.register(models.ReminderType)
admin.site.register(models.Reminder)
admin.site.register(models.Task)
admin.site.register(models.Shopping)
admin.site.register(models.Item)

# Unused, don't display
admin.site.unregister(Group)
