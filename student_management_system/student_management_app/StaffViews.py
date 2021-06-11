from django.contrib import admin
from .models import Attendance, AttendanceReport, CustomUser, SessionStartModel, Students, Subjects
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
def staffHome(request):
    return render(request, "staff_templates/staff_home_template.html")

def studentAttendance(request):
    data = {
        "subjects": Subjects.objects.filter(staff_id=request.user.id),
        "sessions": SessionStartModel.object.all()
    }
    return render(request, "staff_templates/student_attendance_template.html", data)

@csrf_exempt
def getStudents(request):
    subject_id = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")

    print(subject_id, session_year_id)
    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionStartModel.object.get(id=session_year_id)
    students = Students.objects.filter(course_id = subject.course_id, session_year_id=session_model)

    students_details = []
    for student in students:
        # print(student.admin.id)
        temp = {"id": student.admin.id, "name": student.admin.first_name + " " + student.admin.last_name}
        students_details.append(temp)

    final_data = serializers.serialize("python", students)
    return JsonResponse(students_details, content_type="application/json", safe=False)

@csrf_exempt
def saveAttendanceDetails(request):
    student_data = request.POST.get("student_data")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get('session_year')
    subject_id = request.POST.get('subject')

    students_json = json.loads(student_data)
    subject_model = Subjects.objects.get(id=subject_id)
    session_model = SessionStartModel.object.get(id=session_year_id)

    try:
        attendance = Attendance(subject_id=subject_model, session_year_id=session_model, attendance_date=attendance_date)
        attendance.save()

        for stud in students_json:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")

def staffUpdateAttendance(request):
    data = {
        "subjects": Subjects.objects.filter(staff_id=request.user.id),
        "sessions": SessionStartModel.object.all(),
    }
    return render(request, "staff_templates/staff_update_attendance.html", data)

def staffViewAttendance(request):
    return render(request, "staff_templates/staff_view_attendance.html")