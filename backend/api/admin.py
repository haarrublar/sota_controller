from django.contrib import admin
from .models import (MovementRecording, RecordingSession)


# Register your models here.
@admin.register(MovementRecording)
class MovementRecordingAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id','session']
    
@admin.register(RecordingSession)
class RecordingSessionAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id','name']