from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 150)
    name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)

class ProfileModifySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    old_password = serializers.CharField(max_length=100, required = True)
