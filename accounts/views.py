import logging
import re
import secrets

import django
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.views import validate_user_email
from .models import CustomUser


def get_logger():
    logger = logging.getLogger('views_account')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


log = get_logger()
username_pattern = re.compile('^[a-zA-Z0-9_.]+$')


def check_login(request):
    if request.method == 'POST':
        body = request.POST
        username = body['username'].lower()
        password = body['password']
        next_url = body['next']

        user = authenticate(username=username, password=password)

        if user is None:
            log.info(f'{username} cannot be authenticated')
            return render(request, 'registration/login.html',
                          context={'username': username,
                                   'password': password,
                                   'error_login': 'Invalid credentials',
                                   'next': next_url})
        else:
            log.info(f'{username} has just logged in')
            django.contrib.auth.login(request, user)

            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')


def check_regex(pattern, to_check):
    if pattern.match(to_check):
        return True
    else:
        return False


def check_signup(request):
    if request.method == 'POST':
        body = request.POST
        username = body['username'].strip()
        password = body['password'].strip()
        email = body['email'].strip()
        next_url = body['next']

        if CustomUser.objects.filter(username=username):
            log.info(f'username {username} already exists')
            return render(request, 'registration/login.html',
                          context={'error_signup': 'User already exists',
                                   'next': next_url})
        elif not check_regex(username_pattern, username):
            log.info(f'wrong username: {username}')
            return render(request, 'registration/login.html',
                          context={
                              'error_signup': 'username can only contain alphanumeric characters along with . or _',
                              'next': next_url})
        elif not password:
            log.info('empty password')
            return render(request, 'registration/login.html',
                          context={'error_signup': 'empty password',
                                   'next': next_url})
        elif not validate_user_email(email):
            log.info(f'not valid email: {email}')
            return render(request, 'registration/login.html',
                          context={'error_signup': f'not valid email: {email}',
                                   'next': next_url})
        else:
            user = CustomUser(username=username)
            user.set_password(password)
            user.api_key = secrets.token_urlsafe(15)
            user.is_active = False

            user.save()
            log.info(f'{username} has just sign up, sending confirmation email...')

            confirmation_email_text = f"""Hi {user.username},\n\nHere is the link to activate your DataTau account:\n\nhttps://datatau.net/accounts/login/activate/{user.id}/{user.api_key}\n\nWelcome to the coolest Data Science community!\n\nBR,\n\nDavid & Pedro"""
            send_mail(
                subject=f'Confirmation email from datatau.net',
                message=confirmation_email_text,
                from_email='info@datatau.net',
                recipient_list=[email],
                fail_silently=False
            )

            return HttpResponse(
                "<h1>Congrats!</h1><p>You're just one step away to join the DataTau community.</p><p>We've just sent you a confirmation email. Please check your inbox and click on the confirmation link :)</p>")


def activation(request, user_id, api_key):
    if request.method == 'GET':
        user_set = CustomUser.objects.filter(id=user_id)

        if len(user_set) == 1 and user_set[0].api_key == api_key:
            log.info(f'activating user {user_id}...')
            user = user_set[0]
            user.is_active = True
            user.save()

            django.contrib.auth.login(request, user)

        else:
            log.info(f'unable to activate user {user_id}')

        return redirect('index')
