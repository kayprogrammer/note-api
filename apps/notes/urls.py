from django.urls import path
from . import views

urlpatterns = [
    path("", views.NoteListApiView.as_view()),
    path("<uuid:note_id>/", views.NoteApiDetailView.as_view()),
]
