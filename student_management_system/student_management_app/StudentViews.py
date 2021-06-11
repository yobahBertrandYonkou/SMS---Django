from django.http.response import HttpResponse
from django.shortcuts import render


def studentHome(request):
    return render(request, "student_templates/student_home_template.html")