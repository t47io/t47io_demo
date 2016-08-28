from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

import time
import traceback

from filemanager import FileManager

from src.models import *
from src.env import error400, error403


def user_sunetid(request):
    return 'archon'


def user_login(request):
    if request.user.is_authenticated():
        if 'next' in request.GET and 'admin' in request.GET.get('next'):
            return error403(request)
        return HttpResponseRedirect('/group/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        messages = 'Invalid username and/or password. Please try again.'
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            flag = form.cleaned_data['flag']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if flag == "Admin":
                        return HttpResponseRedirect('/admin/')
                    else:
                        return HttpResponseRedirect('/group/')
                else:
                    messages = 'Inactive/disabled account. Please contact us.'
        return render(request, PATH.HTML_PATH['login'], {'form': form, 'messages': messages})
    else:
        if 'next' in request.GET and 'admin' in request.GET.get('next'):
            flag = 'Admin'
        else:
            flag = 'Member'
        form = LoginForm(initial={'flag': flag})
        return render(request, PATH.HTML_PATH['login'], {'form': form})

@login_required
def user_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password_old = form.cleaned_data['password_old']
            password_new = form.cleaned_data['password_new']
            password_new_rep = form.cleaned_data['password_new_rep']
            if password_new != password_new_rep:
                return render(request, PATH.HTML_PATH['password'], {'form': form, 'messages': 'New password does not match. Please try again.'})
            if password_new == password_old:
                return render(request, PATH.HTML_PATH['password'], {'form': form, 'messages': 'New password is the same as current. Please try again.'})

            user = authenticate(username=username, password=password_old)
            if user is not None:
                u = User.objects.get(username=username)
                u.set_password(password_new)
                u.save()
                logout(request)
                return render(request, PATH.HTML_PATH['password'], {'form': form, 'notices': 'Password change successful. Please sign in using new credentials.'})
        form = PasswordForm(initial={'username': request.user.username})
        return render(request, PATH.HTML_PATH['password'], {'form': form, 'messages': 'Invalid username and/or current password, or missing new password.<br/>Please try again.'})
    else:
        form = PasswordForm(initial={'username': request.user.username})
        return render(request, PATH.HTML_PATH['password'], {'form': form})

@login_required
def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                time.sleep(2)
            except ValueError:
                return error400(request)
        else:
            return error400(request)

        return HttpResponseRedirect('/group/contact/')
    else:
        return error400(request)

@login_required
def user_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            time.sleep(2)
            messages = 'success'
        else:
            messages = 'invalid'

        return HttpResponse(simplejson.dumps({'messages': messages}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    else:
        return error400(request)

@login_required
def user_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                time.sleep(4)
                messages = 'success'
            except Exception:
                print traceback.format_exc()
                messages = 'invalid'
        else:
            messages = 'error'

        return HttpResponse(simplejson.dumps({'messages': messages}, sort_keys=True, indent=' ' * 4), content_type='application/json')
    else:
        return render(request, PATH.HTML_PATH['upload'], {'upload_form': UploadForm(), 'messages': ''})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@user_passes_test(lambda u: u.is_superuser)
def browse(request, path):
    fm = FileManager(MEDIA_ROOT + '/data')
    return fm.render(request, path)


