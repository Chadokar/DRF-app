from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework import status
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


class RegisterUserView(GenericAPIView, ObtainAuthToken):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            account = serializer.save()
            user = serializer.data

            print(f'accounts : ', account)
            token, created = Token.objects.get_or_create(user=account)
            user['token'] = token.key

            return Response({
                'data': user,
                'message': f'hi {user["first_name"]} thanks for signing up, a passcode'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, token):
        # Authenticate the user based on the provided token
        print("Received token:", token)

        # Use the TokenAuthentication class to authenticate
        authentication = TokenAuthentication()

        try:
            # Pass the request object only to authenticate, the token should be in the request headers
            user, _ = authentication.authenticate(request)
        except Exception as e:
            print("Authentication error:", e)
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user is authenticated
        if user:
            # Serialize the user data
            serializer = self.serializer_class(user)
            user_data = serializer.data

            return Response({
                'data': user_data,
                'message': f'Hi {user_data["first_name"]}, here is your user data'
            }, status=status.HTTP_200_OK)
        else:
            print("User authentication failed")
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
