from .form import AddStujdentForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Courses, CustomUser, SessionStartModel, Staffs, Students, Subjects
from django.contrib import admin, messages
from django.core.files.storage import FileSystemStorage

def adminHome(request):
    return render(request, "hod_templates/home_content.html", {})

def addStaff(request):
    return render(request, "hod_templates/add_staff_template.html")

def addStaffSave(request):

    if request.method != 'POST':
        return HttpResponse("<h1> Method Not Allowed </h1>")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect("/add_staff/")
        except:
            messages.error(request, "Failed To Add Staff")
            return HttpResponseRedirect("/add_staff/")

def addCourse(request):
    return render(request, "hod_templates/add_course_template.html")

def addCourseSave(request):
    if request.method != 'POST':
           return HttpResponse("<h1> Method Not Allowed </h1>")
    else:
        course_name = request.POST.get("course_name")
        try:
            course_model = Courses.objects.create(course_name=course_name)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect("/add_course/")
        except:
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect("/add_course/")

def addStudent(request):
    data = {
        "form": AddStujdentForm()
    }
    return render(request, "hod_templates/add_student_template.html", data)

def addStudentSave(request):
    form = AddStujdentForm(request.POST, request.FILES)
    if request.method != 'POST':
        return HttpResponse("<h1> Method Not Allowed </h1>")
    else:
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            address = form.cleaned_data["address"]
            course_id = form.cleaned_data["course"]
            session_year = form.cleaned_data["session_year"]
            gender = form.cleaned_data["gender"]
            profile_pic_url = ""

            # if request.FILES.get("profile_pic", False):
            #     profile_pic = request.FILES["profile_pic"]
            #     fileSysStorage = FileSystemStorage()
            #     filename = fileSysStorage.save(profile_pic.name, profile_pic)
            #     profile_pic_url = fileSysStorage.url(filename)

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=3)
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                user.students.address = address
                user.students.session_year_id = SessionStartModel.object.get(id=session_year)
                user.students.gender = gender
                # if profile_pic_url != None:
                #     user.students.profile = profile_pic_url
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect("/add_student/")
            except:
                messages.error(request, "Failed To Add Student")
                return HttpResponseRedirect("/add_student/")
        else:
            form = AddStujdentForm(request.POST)
    return render(request, "hod_templates/add_student_template.html", {"form": form})


def addSubject(request):
    data = {
        "courses": Courses.objects.all().order_by('course_name'),
        "staffs":  CustomUser.objects.filter(user_type=2).order_by('first_name')
    }
    return render(request, 'hod_templates/add_subject_template.html', data)


def addSubjectSave(request):
    if request.method != "POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.create(subject_name=subject_name, course_id=Courses.objects.get(id=course_id), staff_id=CustomUser.objects.get(id=staff_id))
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect("/add_subject/")
        except:
            messages.error(request, "Failed To Add Subject")
            return HttpResponseRedirect("/add_subject/")

def manageStaff(request):
    data = {
        "staffs":  Staffs.objects.all().order_by('created_at')
    }
    return render(request, 'hod_templates/manage_staff_template.html', data)

def manageStudent(request):
    data = {
        "students":  Students.objects.all().order_by('created_at')
    }
    return render(request, 'hod_templates/manage_student_template.html', data)

def manageCourse(request):
    data = {
        "courses":  Courses.objects.all().order_by('created_at')
    }
    return render(request, 'hod_templates/manage_course_template.html', data)

def manageSubject(request):
    data = {
        "subjects":  Subjects.objects.all().order_by('created_at')
    }
    return render(request, 'hod_templates/manage_subject_template.html', data)

def editStaff(request, staff_id):
    data = {
        "staff":  Staffs.objects.get(admin=staff_id),
        "id": staff_id
    }
    return render(request, 'hod_templates/edit_staff_template.html', data)

def editStaffSave(request, staff_id):
    if request.method != "POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")
    else:
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.email = request.POST.get("email")
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.username = request.POST.get("username")
            user.save()

            staff = Staffs.objects.get(admin=staff_id)
            staff.address = request.POST.get("address")
            staff.save()
            messages.success(request, "Successfully Updated Edited Staff")
            return HttpResponseRedirect("/edit_staff/" + staff_id + "/")
        except:
            messages.error(request, "Failed To Edit Staff")
            return HttpResponseRedirect("/edit_staff/" + staff_id + "/")
        

def editStudent(request, student_id):
    data = {
        "student": Students.objects.get(admin=student_id),
        "courses": Courses.objects.all().order_by("created_at"),
        "id": student_id,
        "sessions": SessionStartModel.object.all()
    }
    return render(request, 'hod_templates/edit_student_template.html', data)

def editStudentSave(request, student_id):
    
    if request.method != 'POST':
        return HttpResponse("<h1> Method Not Allowed </h1>")
    else:

        if request.FILES.get("profile_pic", False):
            profile_pic = request.FILES["profile_pic"]
            fileSysStorage = FileSystemStorage()
            filename = fileSysStorage.save(profile_pic.name, profile_pic)
            profile_pic_url = fileSysStorage.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.email = request.POST.get("email")
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.username = request.POST.get("username")
            user.save()
          
            student = Students.objects.get(admin=student_id)
            if profile_pic_url != None:
                student.profile_pic = profile_pic_url
            student.address = request.POST.get("address")
            student.course_id = Courses.objects.get(id=request.POST.get("course"))
            student.session_year_id = SessionStartModel.object.get(id=request.POST.get("session_year"))
            student.gender = request.POST.get("gender")
            student.save()
            
            messages.success(request, "Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/" + student_id)
        except:
            messages.error(request, "Failed To Edit Student")
            return HttpResponseRedirect("/edit_student/" + student_id)


def editSubject(request, subject_id):
    data = {
        "subject": Subjects.objects.get(id=subject_id),
        "staffs": CustomUser.objects.filter(user_type=2).order_by('first_name'),
        "courses": Courses.objects.all().order_by("created_at"),
        "id": subject_id
    }
    return render(request, 'hod_templates/edit_subject_template.html', data)

def editSubjectSave(request, subject_id):
    if request.method != "POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")
    else:
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = request.POST.get('subject_name')
            subject.course_id = Courses.objects.get(id=request.POST.get('course'))
            subject.staff_id = CustomUser.objects.get(id=request.POST.get('staff'))
            subject.save()

            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect("/edit_subject/" + subject_id)
        except:
            messages.error(request, "Failed To Edit Subject")
            return HttpResponseRedirect("/edit_subject/" + subject_id)

def editCourse(request, course_id):
    data = {
        "course": Courses.objects.get(id=course_id),
        "id": course_id
    }
    return render(request, 'hod_templates/edit_course_template.html', data)

def editCourseSave(request, course_id):
    if request.method != 'POST':
           return HttpResponse("<h1> Method Not Allowed </h1>")
    else:
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = request.POST.get("course_name")
            course.save()
            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect("/edit_course/"  + course_id)
        except:
            messages.error(request, "Failed To Edit Course")
            return HttpResponseRedirect("/edit_course/" + course_id)

def addSession(request):
    return render(request, "hod_templates/add_session_template.html")

def addSessionSave(request):
    if request.method != "POST":
        return HttpResponse("<h1>Method Not Allowed</h1>")
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            session =  SessionStartModel.object.create(session_start_year=session_start_year, session_end_year=session_end_year)
            session.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect("/add_session")
        except:
            messages.error(request, "Failed To Add Session")
            return HttpResponseRedirect("/add_session")