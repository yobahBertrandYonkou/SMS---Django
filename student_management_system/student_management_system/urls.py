"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from student_management_system import settings
from student_management_app import views
from django.contrib import admin
from student_management_app import HodViews, StaffViews, StudentViews
from django.urls import path

urlpatterns = [
    path('', views.showLoginPage, name="login"),
    path('get_user_details/', views.getUserDetails, name="get_user_details"),
    path('logout_user/', views.logoutUser, name="logout_user"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('demo/', views.showDemoPage, name="demo"),
    path('admin_home/', HodViews.adminHome, name="admin_home"),
    path('admin/', admin.site.urls),
    path('add_staff/', HodViews.addStaff, name="add_staff"),
    path('add_staff_save/', HodViews.addStaffSave, name="add_staff_save"),
    path('add_course/', HodViews.addCourse, name="add_course"),
    path('add_course_save/', HodViews.addCourseSave, name="add_course_save"),
    path('add_student/', HodViews.addStudent, name="add_student"),
    path('add_student_save/', HodViews.addStudentSave, name="add_student_save"),
    path('add_subject/', HodViews.addSubject, name="add_subject"),
    path('add_subject_save/', HodViews.addSubjectSave, name="add_subject_save"),
    path('manage_staff/', HodViews.manageStaff, name="manage_staff"),
    path('manage_student/', HodViews.manageStudent, name="manage_student"),
    path('manage_course/', HodViews.manageCourse, name="manage_course"),
    path('manage_subject/', HodViews.manageSubject, name="manage_subject"),
    path('edit_staff/<str:staff_id>/', HodViews.editStaff, name="edit_staff"),
    path('edit_staff_save/<str:staff_id>', HodViews.editStaffSave, name="edit_staff_save"),
    path('edit_student/<str:student_id>', HodViews.editStudent, name="edit_student"),
    path('edit_student_save/<str:student_id>', HodViews.editStudentSave, name="edit_student_save"),
    path('edit_subject/<str:subject_id>', HodViews.editSubject, name="edit_subject"),
    path('edit_subject_save/<str:subject_id>', HodViews.editSubjectSave, name="edit_subject_save"),
    path('edit_course/<str:course_id>', HodViews.editCourse, name="edit_course"),
    path('edit_course_save/<str:course_id>', HodViews.editCourseSave, name="edit_course_save"),
    path('add_session/', HodViews.addSession, name="add_session"),
    path('add_session_save/', HodViews.addSessionSave, name="add_session_save"),
    # staff paths
    path('staff_home/', StaffViews.staffHome, name="staff_home"),
    path('student_home/', StudentViews.studentHome, name="student_home"),
    path('student_attendance/', StaffViews.studentAttendance, name="student_attendance"),
    path('get_students/', StaffViews.getStudents, name="get_students"),
    path('save_attendance_details/', StaffViews.saveAttendanceDetails, name="save_attendance_details"),
    path('staff_update_attendance/', StaffViews.staffUpdateAttendance, name="staff_update_attendance"),
    path('staff_view_attendance/', StaffViews.staffViewAttendance, name="staff_view_attendance"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
