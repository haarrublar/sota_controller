from django.db import models

class RecordingSession(models.Model):
    name = models.CharField(max_length=300, default="Sota Control Session")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.started_at}"


class MovementRecording(models.Model):
    """Stores telemetry frames inside a single JSON array per saved recording."""
    session = models.OneToOneField(
        RecordingSession, 
        on_delete=models.CASCADE,
        related_name='recording'
    )
    frames = models.JSONField(default=list)  # Saved only when user hits "Record"
    frame_rate = models.IntegerField(default=60)
    duration_ms = models.IntegerField(default=0)

    def __str__(self):
        return f"Recording for {self.session.name} ({len(self.frames)} frames)"