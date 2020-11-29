from django.contrib import admin
from .models import Courses,CustomUser,Students, Fees, Result, NoticeForStudentOnly,Fee_Record

# Register your models here.
admin.site.register(Courses)
admin.site.register(CustomUser)
admin.site.register(Students)
admin.site.register(Fees)
admin.site.register(Result)
admin.site.register(Fee_Record)
admin.site.register(NoticeForStudentOnly)




