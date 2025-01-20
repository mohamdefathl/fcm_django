from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NotificationSerializer
from fcm_django.firebase_utils import send_notification

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
