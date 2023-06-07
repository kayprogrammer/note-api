from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from . serializers import NoteSerializer
from . models import Note
from apps.common.responses import CustomSuccessResponse

class NoteListApiView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        notes = Note.objects.values("id", "title", "text", "pinned")
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(notes, request)
        return CustomSuccessResponse({"message": "Notes Fetched", "data": paginated_data})
    
class NoteApiDetailView(APIView):
    serializer_class = NoteSerializer

    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs.get('note_id'))
        note_data = {
            "id": note.id,
            "title": note.title,
            "text": note.text,
            "pinned": note.pinned,
        }
        return CustomSuccessResponse({"message": "Note details Fetched", "data": note_data})
    
    def put(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs.get('note_id'))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        for attr, value in data.items():
            setattr(note, attr, value)
        note.save()
        return CustomSuccessResponse({"message": "Note Updated", "data": data})
    
    def delete(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs.get('note_id'))
        note.delete()
        return CustomSuccessResponse({"message": "Note deleted!"})