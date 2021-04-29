from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from . models import PageView,LogoutRegister
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
@login_required
def index(request):
    if not PageView.objects.filter(session=request.session.session_key):
        view = PageView(ip=request.META['REMOTE_ADDR'],created=datetime.datetime.now(),session=request.session.session_key)
        view.save()
    context={"user_number":User.objects.all().count(),"page_views":PageView.objects.all().count(),"sessions_active":Session.objects.filter(expire_date__gt=datetime.datetime.now()).count(),"sessions_inactive":Session.objects.filter(expire_date__lt=datetime.datetime.now()).count(),"logout_register":LogoutRegister.objects.filter(created__startswith=datetime.date.today())[:5]}
    return render(request,"index.html",context)

def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("pwd")
        username=User.objects.get(email=email).username
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            request.session["user"] = username
            return redirect("App:index")
        else:
            messages.add_message(request, messages.INFO,"You have supplied invalid login credentials, please try again!", "danger")
            return render(request, 'login.html')
    return render(request,"login.html")

def register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pwd")
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            messages.add_message(request, messages.INFO,"user with email already exists", "danger")
            return render(request,"register.html")
        else:
            user = User.objects.create(username=username, password=password, email=email)
            user.set_password(user.password)
            user.save()
            messages.add_message(request, messages.INFO,"Registration Succesful", "danger")
    return render(request,"register.html")

def logout(request):
    logout_user=LogoutRegister(username=request.session["user"],created=datetime.datetime.now())
    auth.logout(request)
    logout_user.save()
    messages.add_message(request, messages.INFO," you have been logged out", "danger")
    return redirect("App:login")
