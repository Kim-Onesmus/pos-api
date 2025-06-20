from django.contrib.auth import authenticate
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .serializers import UserCreateSerializer
from rest_framework import status, permissions



@api_view(['POST'])
def register_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'status': 'success',
            'message': 'User created successfully.',
            'code': status.HTTP_201_CREATED,
            'data': {
                'id': str(user.id),
                'username': user.username,
                'role': user.role
            }
        }, status=status.HTTP_201_CREATED)
    else:
        flat_errors = []
        for field_errors in serializer.errors.values():
            flat_errors.extend(field_errors)

        return Response({
            'status': 'error',
            'message': 'User creation failed.',
            'code': status.HTTP_400_BAD_REQUEST,
            'errors': flat_errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({
            'status': 'error',
            'message': 'Username and password are required.',
            'code': status.HTTP_400_BAD_REQUEST,
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if not user:
        return Response({
            'status': 'error',
            'message': 'Invalid username or password.',
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
                'username': user.username,
                "role": user.role
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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get("refresh")

    if refresh_token is None:
        return Response({
            "status": "error",
            "message": "Refresh token is required to logout.",
            "code": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({
            "status": "success",
            "message": "Logout successful. Token blacklisted.",
            "code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({
            "status": "error",
            "message": "Token is invalid or already blacklisted.",
            "code": status.HTTP_400_BAD_REQUEST,
            "details": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
