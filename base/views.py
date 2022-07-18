from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Activities
from .forms import ActivityCreationForm, MyUserCreationForm
from django.contrib.auth.decorators import login_required


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)  # deletes token from the session
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An arror occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    # get activities of the current user
    activities = []
    if request.user.is_authenticated:
        activities = Activities.objects.filter(user=request.user)
    context = {'activities': activities}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def deleteActivity(request, id):
    activity = Activities.objects.get(id=id)
    activity.delete()
    return redirect('home')


@login_required(login_url='login')
def checkActivity(request, id):
    activity = Activities.objects.get(id=id)
    activity.completed = not activity.completed
    activity.save()
    return redirect('home')


@login_required(login_url='login')
def addActivity(request):
    form = ActivityCreationForm()

    if request.method == "POST":
        form = ActivityCreationForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            name, created = Activities.objects.get_or_create(name=name, user=request.user)
            if not created:
                messages.error(request, 'This activity was already created')
                return redirect('home')
            return redirect('home')

    return render(request, 'base/add_activity.html', {'form': form})

            
def meow(request):
    return render(request, 'base/meow.html')