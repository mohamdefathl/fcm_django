from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NotificationSerializer, TokenSerializer
from fcm_django.firebase_utils import send_notification
import random

# Create your views here.

class NotificationAPIView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                response = send_notification(
                    title=serializer.validated_data['title'],
                    body=serializer.validated_data['body'],
                    token=serializer.validated_data.get('token'),
                    topic=serializer.validated_data.get('topic')
                )
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificationCodeAPIView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Generate random 6-digit code
                verification_code = str(random.randint(100000, 999999))
                
                # Send notification with the code
                response = send_notification(
                    title="Verification Code",
                    body=f"Your verification code is: {verification_code}",
                    token=serializer.validated_data['token']
                )
                return Response({
                    "success": True,
                    "message": "Verification code sent successfully",
                    "code": verification_code,
                    **response
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
