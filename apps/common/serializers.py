from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    status = serializers.CharField()
    data = serializers.DictField(required=False)
