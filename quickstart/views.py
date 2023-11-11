from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import User
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegistrationView(generics.CreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            is_staff = request.data.get('is_staff', False)
            is_superuser = request.data.get('is_superuser', False)
            user = serializer.save(is_staff=is_staff, is_superuser=is_superuser)

            user_id = user.id
            iban = user.profile.iban
            account_number = user.profile.account_number
            response_data = {
                'id': user_id,
                'iban': iban,
                'account_number': account_number
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtionUserToken(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(token, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except (InvalidToken, TokenError) as e:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
