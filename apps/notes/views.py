from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .serializers import NoteSerializer
from .models import Note
from apps.common.responses import CustomSuccessResponse, CustomErrorResponse
from apps.common.serializers import ResponseSerializer
from apps.common.custom_methods import IsAuthenticatedCustom


class NoteListApiView(APIView):
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedCustom,)

    @extend_schema(
        summary="List all user notes",
        description="List all notes for the authenticated user",
        parameters=[
            OpenApiParameter(name="pinned", description="Filter by pinned", type=bool)
        ],
        responses=ResponseSerializer,
    )
    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        pinned = request.GET.get("pinned")
        if pinned == "true":
            notes = notes.filter(pinned=True)
        notes = notes.values("id", "title", "text", "pinned")
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(notes, request)
        return CustomSuccessResponse(
            {"message": "Notes Fetched", "data": paginated_data}
        )


class NoteApiDetailView(APIView):
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticatedCustom,)

    @extend_schema(
        summary="Get Note Detail",
        description="Get detail of a particular user note",
        responses=ResponseSerializer,
    )
    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs.get("note_id"))
        if note.user != request.user:
            return CustomErrorResponse({"message": "You cannot see this note!"})
        note_data = {
            "id": note.id,
            "title": note.title,
            "text": note.text,
            "pinned": note.pinned,
        }
        return CustomSuccessResponse(
            {"message": "Note details Fetched", "data": note_data}
        )

    @extend_schema(
        summary="Update Note",
        description="Update a particular user note",
        responses=ResponseSerializer,
    )
    def put(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs.get("note_id"))
        if note.user != request.user:
            return CustomErrorResponse({"message": "You cannot edit this note!"})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        for attr, value in data.items():
            setattr(note, attr, value)
        note.save()
        return CustomSuccessResponse({"message": "Note Updated", "data": data})

    @extend_schema(
        summary="Delete Note",
        description="Delete a particular user note",
        responses=ResponseSerializer,
    )
    def delete(self, request, *args, **kwargs):
        note = get_object_or_404(Note, id=kwargs.get("note_id"))
        if note.user != request.user:
            return CustomErrorResponse({"message": "You cannot delete this note!"})
        note.delete()
        return CustomSuccessResponse({"message": "Note deleted!"})
