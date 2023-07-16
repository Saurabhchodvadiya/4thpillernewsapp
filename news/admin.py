from django.contrib import admin
# from embed_video.admin import AdminVideoMixin
from .models import *


# Register your models here.
class Admin_news(admin.ModelAdmin):
    list_display=('title','delete_status','status','category','date')

    
class Admin_Main_Cat(admin.ModelAdmin):
    list_display=('title','delete_status')

class Admin_Cat(admin.ModelAdmin):
    list_display=('title','delete_status')

# class VideosAdmin(AdminVideoMixin,admin.ModelAdmin):
# 	pass

admin.site.register(Main_category,Admin_Main_Cat)
admin.site.register(Category,Admin_Cat)

admin.site.register(latest_news,Admin_news)

admin.site.register(Videos)
admin.site.register(Donation)
