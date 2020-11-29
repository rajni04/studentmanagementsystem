from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        print(user.is_authenticated and modulename!="django.views.static", "testing")
        if user.is_authenticated and modulename!="django.views.static":
            print(modulename,"the moduansdibasiudb")
            if user.user_type == "1":
                if modulename == "logn.adminview":
                    pass
                elif modulename == "logn.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("homeadmin_template"))
            elif user.user_type == "2":
                if modulename == "logn.FacultyView":
                    pass
                #elif modulename == "logn.views" :
                   # pass
                else:
                    return HttpResponseRedirect(reverse("faculty_home"))

            elif user.user_type == "3":
                
                if modulename == "logn.StudentView"  or modulename == "django.views.static":
                    pass
                elif modulename == "logn.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
                 
        else:
            if request.path == reverse("login") or request.path == reverse("about") or request.path == reverse("contact")   or request.path == reverse("notice_list")   or request.path == reverse("home") or modulename == "django.contrib.auth.views":
                pass
            else:
                pass

        