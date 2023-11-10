import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from .models import User
from .serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            user_id = serializer.data.get('id')
            iban = serializer.data.get('iban')
            account_number = serializer.data.get('account_number')

            response_data = {
                'id': user_id,
                'iban': iban,
                'account_number': account_number
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
