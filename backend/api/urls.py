from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.recording_sessions_list, name='recording-sessions-list'),
    path('sessions/<int:pk>/', views.recording_session_detail, name='recording-session-detail'),
    path('sessions/clear/', views.clear_all_sessions, name='clear-all-sessions'),
    path('controller-events/', views.add_controller_event),        
    path('controller-events/recent/', views.get_recent_events),     
    path('controller-events/clear/', views.clear_events),          
]