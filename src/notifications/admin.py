from django.contrib import admin
from .models import Notification, Chat, Message
# Register your models here.

admin.site.register(Notification)
admin.site.register(Chat)
admin.site.register(Message)