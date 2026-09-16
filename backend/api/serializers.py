from rest_framework import serializers
from .models import RecordingSession, MovementRecording

class MovementRecordingSerializer(serializers.ModelSerializer):
    total_frames = serializers.SerializerMethodField()

    class Meta:
        model = MovementRecording
        fields = ['id', 'frames', 'frame_rate', 'duration_ms', 'total_frames']

    def get_total_frames(self, obj):
        return len(obj.frames) if isinstance(obj.frames, list) else 0


class RecordingSessionSerializer(serializers.ModelSerializer):
    recording = MovementRecordingSerializer(read_only=True)
    total_frames = serializers.SerializerMethodField()

    class Meta:
        model = RecordingSession
        fields = ['id', 'name', 'started_at', 'ended_at', 'total_frames', 'recording']

    def get_total_frames(self, obj):
        if hasattr(obj, 'recording') and isinstance(obj.recording.frames, list):
            return len(obj.recording.frames)
        return 0