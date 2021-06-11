from django.contrib.auth import login, logout
from .EmailBackEnd import EmailBackEnd
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def showDemoPage(request):
    return render(request, 'demo.html', {})

def showLoginPage(request):
    return render(request, 'login.html', {})

def doLogin(request):
    if request.method != 'POST':
        return HttpResponse("<h1>Request Not Allowed</h1>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home/')
                
            if user.user_type == "2":
                return HttpResponseRedirect("/staff_home")

            if user.user_type == "3":
                return HttpResponseRedirect("/student_home")

        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")

def getUserDetails(request):

    if request.user == None:
        return HttpResponse("<h1>User not logged In</h1>")

    else:
        return HttpResponse("User: " + request.user.email + " usertype " + request.user.user_type)

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect("/")