from rest_framework import serializers

class NoteSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=300)
    text = serializers.CharField()    
    pinned = serializers.BooleanField()

