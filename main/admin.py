from django.contrib import admin
from .models import FriendsList,chatRoom,Messages,RequestList
# Register your models here.


admin.site.register(chatRoom)
admin.site.register(Messages)
admin.site.register(FriendsList)
admin.site.register(RequestList)
