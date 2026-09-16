from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import RecordingSession, MovementRecording
from .serializers import RecordingSessionSerializer, MovementRecordingSerializer
from django.core.cache import cache
from time import time


@api_view(['GET'])
@permission_classes([AllowAny])
def recording_sessions_list(request):
    """
    Get all recorded sessions.
    """
    if request.method == 'GET':
        sessions = RecordingSession.objects.all().order_by('-started_at')
        serializer = RecordingSessionSerializer(sessions, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([AllowAny])
def recording_session_detail(request, pk):
    """
    Get or delete a single recording session (includes nested movement data).
    """
    try:
        session = RecordingSession.objects.get(pk=pk)
    except RecordingSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecordingSessionSerializer(session)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        session.delete()
        return Response({'message': 'Session deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def movement_recording_list(request):
    """
    Get all movement recordings.
    """
    if request.method == 'GET':
        recordings = MovementRecording.objects.all()
        serializer = MovementRecordingSerializer(recordings, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def movement_recording_detail(request, pk):
    """
    Get a specific movement recording directly by its own ID.
    """
    try:
        recording = MovementRecording.objects.get(pk=pk)
    except MovementRecording.DoesNotExist:
        return Response({'error': 'Movement recording not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovementRecordingSerializer(recording)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_all_sessions(request):
    """
    Delete all sessions (cascades and purges all movement recordings).
    """
    if request.method == 'DELETE':
        count, _ = RecordingSession.objects.all().delete()
        return Response(
            {"message": f"Successfully deleted {count} recording sessions."},
            status=status.HTTP_200_OK
        )
        
        
BUFFER_KEY = "recent_controller_events"
WINDOW_SECONDS = 60  # 5 minutes


def _get_trimmed_buffer():
    events = cache.get(BUFFER_KEY, [])
    cutoff = time() - WINDOW_SECONDS
    trimmed = [e for e in events if e["t"] >= cutoff]
    return trimmed


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def add_controller_event(request):
    events = _get_trimmed_buffer()
    events.append({
        "t": time(),
        "type": request.data.get("type"),
        "name": request.data.get("name"),   # for button events
        "data": request.data.get("data"),   # for axes events
    })
    cache.set(BUFFER_KEY, events, timeout=WINDOW_SECONDS)
    return Response({"status": "ok"})


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def get_recent_events(request):
    # get data form cache
    return Response(_get_trimmed_buffer())


@api_view(['GET','POST','DELETE'])
@permission_classes([AllowAny])
def clear_events(request):
    cache.delete(BUFFER_KEY)
    return Response({"status": "cleared"})