from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from django.shortcuts import render


class LoginAPIView(APIView):
    """
    The purpose of this APIView is so that bots can authenticate via REST
    """
    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
