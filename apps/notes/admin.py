from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "pinned", "created_at", "updated_at")
    list_filter = ("user", "title", "pinned", "created_at", "updated_at")


admin.site.register(Note, NoteAdmin)
