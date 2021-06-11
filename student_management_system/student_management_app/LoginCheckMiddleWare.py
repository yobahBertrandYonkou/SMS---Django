from django.http.response import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "student_management_app.HodViews":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "student_management_app.StaffViews":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                if modulename == "student_management_app.views":
                    pass
                elif modulename == "student_management_app.StudentViews" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
        else:
            if request.path == reverse("login") or request.path == reverse("doLogin"):
                pass
            else:
                return HttpResponseRedirect(reverse("login"))