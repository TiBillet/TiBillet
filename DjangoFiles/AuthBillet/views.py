import json

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from django.utils.translation import ugettext_lazy as _

from ApiBillet.views import request_for_data_cashless
from AuthBillet.models import TibilletUser
from rest_framework_simplejwt.tokens import RefreshToken

from AuthBillet.serializers import MeSerializer, CreateUserValidator
from AuthBillet.utils import validate_email_and_return_user
from BaseBillet.models import Configuration

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from BaseBillet.tasks import connexion_celery_mailer

User = get_user_model()


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))


'''
from djoser.conf import settings as djoser_settings
from djoser import utils
from djoser.views import UserViewSet, TokenCreateView
EX DJOSER MODEL
class TokenCreateView_custom(TokenCreateView):
    """
    Use this endpoint to obtain user authentication token.
    """

    serializer_class = djoser_settings.SERIALIZERS.token_create
    permission_classes = djoser_settings.PERMISSIONS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = djoser_settings.SERIALIZERS.token

        # on modifie la creation du token pour rajouter access_token dans la réponse pour Postman
        data_response = token_serializer_class(token).data
        data_response['access_token'] = data_response.get('auth_token')
        # import ipdb; ipdb.set_trace()
        print(f'data_response {data_response}')
        return Response(
                data=data_response, status=status.HTTP_200_OK
            )
'''


class activate(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token):
        user = User.objects.get(pk=decode_uid(uid))
        if user.email_error:
            return Response('Mail non valide', status=status.HTTP_406_NOT_ACCEPTABLE)

        PR = PasswordResetTokenGenerator()
        is_token_valid = PR.check_token(user, token)
        # print(user)
        if is_token_valid:
            user.is_active = True
            refresh = RefreshToken.for_user(user)
            user.save()
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response('Token non valide', status=status.HTTP_400_BAD_REQUEST)




class create_user(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        validator = CreateUserValidator(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = validator.validated_data.get('email').lower()
        password = validator.validated_data.get('password')

        user = validate_email_and_return_user(email, password)

        if user :
            return Response(_('Pour acceder à votre espace et réservations, merci de valider votre adresse email. Pensez à regarder dans les spams !'),
                            status=status.HTTP_200_OK)
        else :
            return Response(_("Email non valide. Merci de vérifier votre email."), status=status.HTTP_406_NOT_ACCEPTABLE)



class MeViewset(viewsets.ViewSet):

    def list(self, request):
        serializer = MeSerializer(request.user)
        serializer_copy = serializer.data.copy()

        configuration = Configuration.get_solo()
        if configuration.server_cashless and configuration.key_cashless:
            serializer_copy['cashless'] = request_for_data_cashless(request.user)

        return Response(serializer_copy, status=status.HTTP_200_OK)



    def get_permissions(self):
        if self.action in ['list', ]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
