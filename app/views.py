from django.contrib.auth import authenticate
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response({
            'status': 'error',
            'message': 'Email and password are required.',
            'code': status.HTTP_400_BAD_REQUEST,
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)

    if not user:
        return Response({
            'status': 'error',
            'message': 'Invalid email or password.',
            'code': status.HTTP_401_UNAUTHORIZED,
            'data': None
        }, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({
        'status': 'success',
        'message': 'Login successful.',
        'code': status.HTTP_200_OK,
        'data': {
            'user': {
                'id': str(user.id),
                'email': user.email
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    serializer = TokenRefreshSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data.get('access')

        return Response({
            'status': 'success',
            'message': 'Token refreshed successfully.',
            'code': status.HTTP_200_OK,
            'data': {
                'access_token': access_token
            }
        }, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({
            'status': 'error',
            'message': 'Invalid or expired refresh token.',
            'code': status.HTTP_401_UNAUTHORIZED,
            'data': {
                'error': str(e)
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
