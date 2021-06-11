from django.db import models
from django.db.models.fields import DateField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
# Create your models here.

class SessionStartModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    object = models.Manager()

class CustomUser(AbstractUser):
    user_type_data = (
        (1, "HOD"),
        (2, "Staff"),
        (3, "Student")
    )

    user_type = models.CharField(default=1, max_length=255, choices=user_type_data)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.TextField(max_length=255)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=255)
    profile_pic = models.FileField()
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField(max_length=255)
    session_year_id = models.ForeignKey(SessionStartModel, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    session_year_id = models.ForeignKey(SessionStartModel, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_status = models.BooleanField(default=False)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class LeaveReportStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_status = models.BooleanField(default=False)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class FeedBackStudents(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

class NotificationStudents(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects =  models.Manager()

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance, address="")
        
        if instance.user_type == 3:
            Students.objects.create(admin=instance, course_id=Courses.objects.get(id=1), session_year_id=SessionStartModel.object.get(id=1), address="", profile_pic="")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()

    if instance.user_type == 2:
        instance.staffs.save()
 
    if instance.user_type == 3:
        instance.students.save()
