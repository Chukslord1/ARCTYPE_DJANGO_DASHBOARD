from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from . models import Event,RegisterEvent,LoginEvent,ViewPageEvent,EditProfileEvent,LogoutEvent,Analytics
from django.contrib.sessions.models import Session
import datetime

#query to classify events into seperate tables
for i in Event.objects.all():
    if i.name == "Registered":
        if RegisterEvent.objects.filter(username=i.username,created=i.created):
            pass
        else:
            register=RegisterEvent(username=i.username,created=i.created)
            register.save()
    if i.name == "Logged In":
        if LoginEvent.objects.filter(username=i.username,created=i.created):
            pass
        else:
            login=LoginEvent(username=i.username,created=i.created)
            login.save()
    if i.name == "Viewed Page":
        if ViewPageEvent.objects.filter(ip=i.ip,session=i.session,created=i.created):
            pass
        else:
            page=ViewPageEvent(ip=i.ip,session=i.session,created=i.created)
            page.save()
    if i.name == "Edited Profile":
        if EditProfileEvent.objects.filter(username=i.username,created=i.created):
            pass
        else:
            edit=EditProfileEvent(username=i.username,created=i.created)
            edit.save()
    if i.name == "Logged Out":
        if LogoutEvent.objects.filter(username=i.username,created=i.created):
            pass
        else:
            logout=LogoutEvent(username=i.username,created=i.created)
            logout.save()

#query to make the analytics data for arctype dashboard
if Analytics.objects.filter(name="Number of Registered Users"):
    analytics=Analytics.objects.get(name="Number of Registered Users")
    analytics.stats=RegisterEvent.objects.all().count()
    analytics.date=datetime.datetime.now()
    analytics.save()
else:
    analytics = Analytics.objects.create(name="Number of Registered Users")
    analytics.save()

if Analytics.objects.filter(name="Number of Users that Logged In"):
    analytics=Analytics.objects.get(name="Number of Users that Logged In")
    analytics.stats=LoginEvent.objects.all().count()
    analytics.date=datetime.datetime.now()
    analytics.save()
else:
    analytics = Analytics.objects.create(name="Number of Users that Logged In")
    analytics.save()

if Analytics.objects.filter(name="Number of Users that Logged Out"):
    analytics=Analytics.objects.get(name="Number of Users that Logged Out")
    analytics.stats=LogoutEvent.objects.all().count()
    analytics.date=datetime.datetime.now()
    analytics.save()
else:
    analytics = Analytics.objects.create(name="Number of Users that Logged Out")
    analytics.save()

if Analytics.objects.filter(name="Number of Users that Edited their Profile"):
    analytics=Analytics.objects.get(name="Number of Users that Edited their Profile")
    analytics.stats=EditProfileEvent.objects.all().count()
    analytics.date=datetime.datetime.now()
    analytics.save()
else:
    analytics = Analytics.objects.create(name="Number of Users that Edited their Profile")
    analytics.save()

if Analytics.objects.filter(name="Number of the Profile Page Views"):
    analytics=Analytics.objects.get(name="Number of the Profile Page Views")
    analytics.stats=ViewPageEvent.objects.all().count()
    analytics.date=datetime.datetime.now()
    analytics.save()
else:
    analytics=Analytics.objects.create(name="Number of the Profile Page Views")
    analytics.save()



# Create your views here.
def index(request):
    profile=request.user
    if not Event.objects.filter(session=request.session.session_key):
        view = Event(name="Viewed Page",ip=request.META['REMOTE_ADDR'],created=datetime.datetime.now(),session=request.session.session_key)
        view.save()
    if request.method=="POST":
        email=request.POST.get("email")
        username=request.POST.get("username")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        if email:
            profile.email=email
        if username:
            profile.username=username
        profile.first_name=first_name
        profile.last_name=last_name
        profile.save()
        edit=Event(name="Edited Profile",username=request.user,created=datetime.datetime.now())
        edit.save()
    context={"profile":profile}
    return render(request,"index.html",context)

def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("pwd")
        username=User.objects.get(email=email).username
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session["user"] = username
            login_user=Event(name="Logged In",username=request.session["user"],created=datetime.datetime.now())
            login_user.save()
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
            register_user=Event(name="Registered",username=username,created=datetime.datetime.now())
            register_user.save()
            messages.add_message(request, messages.INFO,"Registration Succesful", "danger")
    return render(request,"register.html")

def logout(request):
    logout_user=Event(name="Logged Out",username=request.session["user"],created=datetime.datetime.now())
    auth.logout(request)
    logout_user.save()
    messages.add_message(request, messages.INFO," you have been logged out", "danger")
    return redirect("App:login")
