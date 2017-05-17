from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from blog2.core.decorator import is_anonymous
from django.contrib.auth.decorators import login_required
from django.conf import settings


def singup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request,
                             'New user has been created %s.' % user.username)
    return render(request, 'core/singup.html', locals())


@is_anonymous
def singin(request):
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    return render(request, 'core/singin.html', locals())


@login_required
def singout(request):
    logout(request)
    return redirect('main')
