from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from core.models import User, Member
from core.serializers.signup import SignupSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={200: 'Signup successful', 400: 'Invalid data'}
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                name = serializer.validated_data['name']
                email = serializer.validated_data['email']
                with transaction.atomic():
                    user = User.objects.create_user(username=username, password=password)
                    Member.objects.create(user=user, name=name, email=email)

                    return Response({'message': 'Signup successful'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
