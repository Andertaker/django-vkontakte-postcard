# -*- coding: utf-8 -*-
from django.contrib import admin

from . models import Postcard



class PostcardAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'sender_name', 'receiver_name', 'photo', 'comment', 'created_at', 'updated_at')
    #list_filter = ('sender_id',)


admin.site.register(Postcard, PostcardAdmin)

