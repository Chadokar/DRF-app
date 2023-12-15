from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated


from rest_framework import status
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     # This view is accessible only to authenticated users
    #     return Response({'message': 'You are authenticated!'})
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user_id = token.user.id
                email = token.user.email
                last_login = token.user.last_login
                date_joined = token.user.date_joined
                is_active = token.user.is_active

                full_name = token.user.first_name + ' ' + token.user.last_name
                return Response({
                    'user_id': user_id,
                    'full_name': full_name,
                    'email': email, 'last_login': last_login,
                    'date_joined': date_joined,
                    'is_active': is_active
                })
            except Token.DoesNotExist:
                return Response({'error': 'Invalid token'}, status=400)
        else:
            return Response({'error': 'Token not provided'}, status=400)


class UserLoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'full_name': user.first_name + ' ' + user.last_name,
                'last_login': user.last_login,
                'date_joined': user.date_joined,
                'is_active': user.is_active
            })
        else:
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(GenericAPIView, ObtainAuthToken):
    serializer_class = UserSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            account = serializer.save()
            user = serializer.data
            return Response(data={
                'data': user,
                'success': True
            })

            # print(f'accounts : ', account)
            # token, created = Token.objects.get_or_create(user=account)
            # user['token'] = token.key

            # return Response({
            #     'message': f'hi {user["first_name"]} thanks for signing up, a passcode'
            # }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(GenericAPIView):

    serializer_class = UserSerializer

    def getuser(self, data): return self.serializer_class(data)

    def get(self, request):
        return Response({'data': self.getuser(request.data)})

    def put(self, request):
        data = request.data
        first_name = data['first_name']
