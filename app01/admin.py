from django.contrib import admin
from app01.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(ChatHistory)
admin.site.register(ChatFriend)
admin.site.register(GroupFriend)