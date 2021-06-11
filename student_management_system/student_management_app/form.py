from django import forms
from django.forms.widgets import PasswordInput, Select
from .models import Courses, SessionStartModel

class DateInput(forms.DateInput):
    input_type = "date"

class AddStujdentForm(forms.Form):
    # try:
    courses_obj = Courses.objects.all()
    courses = []

    for course in courses_obj:
        temp = (course.id, course.course_name)
        courses.append(temp)
    # except:
    #     courses = []

    # try:
    sessions_obj = SessionStartModel.object.all()
    sessions = []

    for session in sessions_obj:
        temp = (session.id, str(session.session_start_year) + "  TO  " + str(session.session_end_year))
        sessions.append(temp)
    # except:
    #     sessions = []
        

    email = forms.EmailField(label = "Email Address", max_length=100,widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=100,widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=100,widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=100,widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=100,widget=forms.TextInput(attrs={"class": "form-control"}))
    course = forms.ChoiceField(label="Course", choices=courses,widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=[("Male", "Male"),("Female", "Female")],widget=forms.Select(attrs={"class": "form-control"}))
    session_year = forms.ChoiceField(label="Session Year", choices=sessions, widget=Select(attrs={"class": "form-control"}))
    # profile_pic = forms.FileField(label="Profile Pic", max_length=100)