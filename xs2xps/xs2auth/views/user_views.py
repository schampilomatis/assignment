from __future__ import absolute_import
import logging
import json
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from random import uniform
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.db import IntegrityError
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from .. import serializers
from ..models import ExpiringToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template import loader
from django.conf import settings
from ..auth import CustomBasicAuthentication, ProviderAuthentication
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
from django.http import JsonResponse
User = get_user_model()


@api_view(['POST'])
@authentication_classes((CustomBasicAuthentication, ProviderAuthentication,))
def login(request, format=None):
    data = serializers.UserSerializer(request.user).data
    token = ExpiringToken.get_or_create_if_expired(user=request.user)
    data['token'] = token.key
    return JsonResponse(data)


@api_view(['GET', 'POST'])
def logout_view(request):
    user = request.user
    logout(request)
    ExpiringToken.objects.filter(user=user).delete()
    return JsonResponse({})


def weblogin(_):
    return render_to_response('xs2auth/login.html')


@api_view(['POST'])
@permission_classes([AllowAny,])
def register(request):
    try:
        data = json.loads( request.body )
    except ValueError:
        raise APIException('JSON_INVALID', 403)
    user = User()

    try:
        user.username = data['email']  # change it to specific requirements
        password = data['password']
    except KeyError:
        raise APIException('REGISTRATION_DATA_NOT_VALID', 403)
    user.name = data.get('name')
    user.lastname = data.get('lastname')
    user.email = data.get('email')
    user.set_password(password)
    user.provider = 'local'

    #Save now to create the profile
    user.coordinates = Point(5.025190989375114 + (uniform(0, 1) / 10) - 0.05, 52.290536298044026 + (uniform(0, 1) / 10) - 0.05)

    try:
        user.full_clean()
        user.save()
    except IntegrityError:
        raise APIException('USER_EXIST', 403)
    except ValidationError:
        raise APIException('REGISTRATION_DATA_NOT_VALID', 403)

    token = ExpiringToken.get_or_create_if_expired(user=user)
    return_data = serializers.UserSerializer(user).data
    return_data['token'] = token.key
    try:
        send_mail('From XS2 Framework', 'Your email address has just been used to register a user to XS2. If you have any questions, please contact support@xs2theworld.com', 'support@xs2theworld.com',
            [user.email], fail_silently=False)
    except Exception, e:
        #log something here
        pass
    return JsonResponse(return_data)


@api_view(['POST'])
@permission_classes([AllowAny,])
def request_password_reset(request, format=None):
    try:
        data = json.loads( request.body )
    except:
        raise APIException('JSON_INVALID', 400)

    email = data.get("email")
    if email == None:
        raise APIException('NO_AUTH_DATA', 400)

    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist:
        raise APIException('USER_DOES_NOT_EXIST', 400)

    template_data = {
        'email': user.email,
        'domain': request.META['HTTP_HOST'],
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }

    email_subject = loader.render_to_string('password_reset_email_subject.txt', template_data)
    # subject cannot contain \n
    email_subject = ''.join(email_subject.splitlines())
    email_body = loader.render_to_string('password_reset_email_body.html', template_data)
    send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
    return JsonResponse({})


@api_view(['POST', 'GET'])
@permission_classes([AllowAny,])
def reset_password_confirm(request, uidb64=None, token=None, *arg, **kwargs):

    if request.method == 'GET':
        return render(request,'password_reset.html', {'uidb64': uidb64, 'token': token})

    try:
        data = json.loads( request.body )
        new_pass = data.get('password')
        is_api_call = True
    except:
        new_pass = request.POST.get('password')
        is_api_call = False

    if not new_pass:
        APIException('NO_AUTH_DATA', 400)

    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise APIException('AUTHENTICATION_DATA_NOT_VALID', 403)

    if default_token_generator.check_token(user, token):
        user.set_password(new_pass)
        user.save()
    else:
        raise APIException('AUTHENTICATION_DATA_NOT_VALID', 403)

    if is_api_call:
        return JsonResponse({})
    else:
        return render(request,'password_reset_success.html')
