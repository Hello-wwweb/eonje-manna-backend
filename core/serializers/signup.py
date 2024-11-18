from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)


