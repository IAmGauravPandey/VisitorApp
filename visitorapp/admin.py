from django.contrib import admin
from .models import *

class VisitAdmin(admin.ModelAdmin):
    list_display=('user','host_name','host_email','host_phone','checkin','checkout')
admin.site.register(UserProfile)
admin.site.register(Visit,VisitAdmin)
admin.site.register(Host)
admin.site.site_header='Management'
