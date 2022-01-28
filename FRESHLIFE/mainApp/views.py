from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


def mainPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    else:
        return render(request, 'mainApp/mainPage.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('mainApp:mainPage')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')


