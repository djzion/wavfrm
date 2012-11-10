from django.contrib import admin
from models import *

class TrackAdmin(admin.ModelAdmin):
    model = Track

admin.site.register(Track, TrackAdmin)