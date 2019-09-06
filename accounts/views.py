import logging
import re
import secrets

import django
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

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
username_pattern = re.compile('^[a-zA-Z0-9_.-]+$')
password_pattern = re.compile('^[A-Za-z0-9@#$%^&+=]+$')


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
        next_url = body['next']

        if CustomUser.objects.filter(username=username):
            log.info(f'{username} already exists')
            return render(request, 'registration/login.html',
                          context={'error_signup': 'User already exists',
                                   'next': next_url})
        elif not check_regex(username_pattern, username):
            log.info(f'wrong {username}')
            return render(request, 'registration/login.html',
                          context={'error_signup': 'not ^[a-zA-Z0-9_.-]+$ user',
                                   'next': next_url})
        elif not check_regex(password_pattern, password):
            log.info(f'wrong {password}')
            return render(request, 'registration/login.html',
                          context={'error_signup': 'not ^[A-Za-z0-9@#$%^&+=]+$ password',
                                   'next': next_url})
        else:
            user = CustomUser(username=username)
            user.set_password(password)
            user.api_key = secrets.token_urlsafe(15)

            user.save()
            log.info(f'{username} has just sign up')

            django.contrib.auth.login(request, user)

            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
