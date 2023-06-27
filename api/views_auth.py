from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class Login(APIView):
    """
    username    
    password
    """
    permission_classes = []

    def get(self, request):
        return Response({'username': 'username', 'password': 'password'})

    def post(self, request: Request):
        username = request.data.get("username")
        user = User.objects.filter(username=username).first()

        if not user:
            return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(data={"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        Token.objects.filter(user=user).delete()
        Token.objects.create(user=user)
        response = {"message": "Login Successfull", "token": user.auth_token.key}
        return Response(data=response, status=status.HTTP_200_OK)


class IsTokenValid(APIView):
    permission_classes = []

    def post(self, request: Request):
        token = request.data.get('token')
        return Response(data={'message': Token.objects.filter(key=token).first() is not None})
