import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from SOTA.sota_controller.backend.api.models import RecordingSession, MovementRecording

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_recording = False
        self.current_session = None
        self.frame_buffer = []

    def handle_start_recording(self, session_name="Controller Session"):
        self.current_session = RecordingSession.objects.create(
            name=session_name,
            started_at=timezone.now()
        )
        self.frame_buffer = []
        self.is_recording = True
        print(f"Started session ID: {self.current_session.id}")

    def handle_incoming_frame(self,controller_state):
        if self.is_recording:
            self.frame_buffer.append(controller_state)

    def handle_stop_recording(self):
        if not self.is_recording or not self.current_session:
            return

        self.is_recording = False
        
        self.current_session.ended_at = timezone.now()
        self.current_session.save()

        duration_ms = len(self.frame_buffer) * (1000 // 60)

        MovementRecording.objects.create(
            session=self.current_session,
            frames=self.frame_buffer,
            frame_rate=60,
            duration_ms=duration_ms
        )
        
        print(f"Saved {len(self.frame_buffer)} frames to Session {self.current_session.id}")
        
        self.current_session = None
        self.frame_buffer = []
        
    def handle(self, *args, **options):
            print("Telemetry management command active.")