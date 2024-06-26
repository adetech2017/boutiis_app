from django.contrib import admin
from forum.models import LiveForum# Register your models here.



class LiveForumAdmin(admin.ModelAdmin):
    pass


admin.site.register(LiveForum, LiveForumAdmin)