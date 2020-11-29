from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages 
from logn.models import  CustomUser, Courses ,Faculty ,Students,SessionYearModel
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from logn.models import Result,Courses,Fee_Record,CustomUser,Subjects,Students,SessionYearModel,Attendance,Faculty,AttendanceReport,Department,FeedBackStudent,Fees,Fee_payment,NoticeForStudentOnly
import datetime
from django.contrib.auth import authenticate, logout
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm


def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    course=Courses.objects.get(id=student_obj.course_id.id)
    pending_amt= course.fee_record_set.filter(student_id=student_obj)[0].pending
    print(pending_amt, course)
    subjects=Subjects.objects.filter(course_id=course).count()
   # fee=Fee_Record.objects.filter(fee_record_id=student_obj.pending)
 #   notice_count=NoticeForStudentOnly.objects.filter(course_id=course).count()
    notice_total=NoticeForStudentOnly.objects.filter(course_id=student_obj.course_id, seen=False).count()
    return render(request,"logn/Student_template/homestudent_template.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subjects":subjects,'notice_total':notice_total,'pending':pending_amt})



# ALTER TABLE logn_noticeforstudentonly ADD COLUMN seen character varying(50) NOT NULL DEFAULT 'someName'



"""def add1(request):
   
    student=Students.objects.get(admin_id=request.user.id)
    print("Email : "+student.admin.email)
    course=Courses.objects.all()
    sessionyear=SessionYearModel.object.all()
    return render(request,"logn/Student_template/add_student.html",{"course":course,'student': student,'sessionyear':sessionyear})


def add1_save(request): 
   if request.method!="POST":
        return HttpResponse("Method Not Allowed")
   else:    
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
            
        email=request.POST.get("email")
        date=request.POST.get("date")
        phno=request.POST.get("phno")
           
        address=request.POST.get("address")
        session_year_id=request.POST.get("session_year_id")
        course_id=request.POST.get("course")
        gender=request.POST.get("gender")
        profile_pic=request.FILES['profile_pic']
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
        #try:
       
        admin=CustomUser.objects.get(id=request.user.id)
        user=Students.objects.get(admin=admin)
        user.address=address
        user.dob=date
        user.phno=phno
        course_obj=Courses.objects.get(id=course_id)
        user.course_id=course_obj
        session_year=SessionYearModel.object.get(id=session_year_id)
        user.gender=gender
        user.profile_pic=profile_pic_url
        user.save()

        admin.first_name=first_name
        admin.last_name=last_name
        admin.save()
        messages.success(request,"Successfully Added Student")
        return HttpResponse("ok")
         #   return HttpResponseRedirect("add1")
        #except:
         #   return HttpResponseRedirect("logn/add1")"""
        

"""def add1_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
    
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
            
        email=request.POST.get("email")
        date=request.POST.get("date")
        phno=request.POST.get("phno")
           
        address=request.POST.get("address")
        session_start=request.POST.get("session_start")
        session_end=request.POST.get("session_end")
        course_id=request.POST.get("course")
        gender=request.POST.get("gender")
        profile_pic=request.FILES['profile_pic']
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
           
        try:
            user=CustomUser.objects.update_user( username=username , password=None, email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.students.address=address
            user.students.dob=date
            user.students.phno=phno
            course_obj=Courses.objects.get(id=course_id)
            user.students.course_id=course_obj
            user.students.session_start_year=session_start
            user.students.session_end_year=session_end
            user.students.gender=gender
            user.students.profile_pic=profile_pic_url
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect("add1")
        except:
              messages.error(request,"Failed to Add Student")
              return HttpResponseRedirect("logn/add1")"""

"""def student_view(request):
    student=Students.objects.all()
    return render(request,"logn/Student_template/student_view.html",{'student': student})"""




def edit_student(request,student_id):
    course=Courses.objects.all()
    student=Students.objects.get(admin=student_id)
    return render(request,"logn/Student_template/student_edit.html",{"student":student,"course":course})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        date=request.POST.get("date")
        phno=request.POST.get("phno")
        address = request.POST.get("address")
        session_year_id=request.POST.get("session_year_id")
        course_id = request.POST.get("course")
        gender = request.POST.get("gender")

        
        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.email=email
            user.save()

            student=Students.objects.get(admin=student_id)
            student.address=address
            student.date=date
            student.phno=phno
            session_year=SessionYearModel.object.get(id=session_year_id)
            student.gender=gender
            course=Courses.objects.get(id=course_id)
            student.course_id=course
            
            student.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/"+student_id)
        except:
            messages.error(request,"Failed to Edit Student")
            return HttpResponseRedirect("/edit_student/"+student_id)

def delete_student(request,student_id):
    student=Students.objects.get(id=student_id)
    student.delete()
    return redirect("/student_view")


def give_feedback(request):
    student_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=student_id)
    
    department=Department.objects.all()
    faculty=Faculty.objects.all()
    
    return render(request,"logn/Student_template/feedback.html",{'departments':department,'facultys':faculty,'feedback_data':feedback_data})

# delete this if it doesn't work
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json
def fetch_api(request, department_id):
    dep=Department.objects.get(id=department_id).faculty_set.all()
    print(Department.objects.get(id=department_id).faculty_set.all())
    data=[]
    for i in dep:
        data.append({"id":i.pk, "first_name":i.admin.first_name, "last_name":i.admin.last_name})
    
    # data=serializers.serialize(
    #                 'json', data)
    print(data)
    return HttpResponse(json.dumps(data), content_type="application/json")



def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request,"logn/Student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_object)

    
    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,"logn/Student_template/student_attendance.html",{"attendance_reports":attendance_reports})
    
    
def feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")
        student_obj=Students.objects.get(admin=request.user.id)
        department_id=request.POST.get("department")
        department=Department.objects.get(id=department_id)
        faculty_id=request.POST.get("faculty")
        faculty=Faculty.objects.get(id=faculty_id)
        
        
        #try:
        feedback=FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="",faculty_id=faculty,department_id=department)
        feedback.save()
        messages.success(request, "Successfully Sent Feedback")
        return HttpResponseRedirect(reverse("give_feedback"))
        #except:
            #messages.error(request, "Failed To Send Feedback")
            #return HttpResponseRedirect(reverse("give_feedback"))

def fee_payment(request): 
    course=Courses.objects.all()
    
    return render(request,"logn/Student_template/fee_payment.html",{'course':course})

def fee_payment_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        
        course_id=request.POST.get("course")
       
        amount=request.POST.get("amount")
        date = request.POST.get("date")
        course_obj=Courses.objects.get(id=course_id)

        #try:
        fee_payment=Fee_payment(amount=amount, date=date, course_id=course_obj)
        fee_payment.course_id=course_obj   
        print(Students.objects.get(id=request.session["user"]))
        fee_payment.student_id = Students.objects.get(id=request.session["user"])

        fee_payment.save()
        print(fee_payment)
        messages.success(request,"Successfully Edited Subject")
        return HttpResponseRedirect(reverse("fee_payment"))
       # except:
          #  messages.error(request,"Failed to Edit Subject")
           # return HttpResponseRedirect(reverse("fee_payment"))

def pay(request): 
    if request.method == "POST":
        return render(request,"logn/Student_template/pay.html")

def course_fetch(request, course_id):
    if request.method =="GET":
        try:
            course = Courses.objects.get(id=course_id)
            print(course)
            fee = course.fees_set.all()
            print(fee[0])
            data = [{"fee": fee[0].tot_amount}]
        except Exception as e:
            print(e)
            data={"error": str(e)}
    return HttpResponse(json.dumps(data), content_type="application/json")





def view_result(request):
    if request.method == "GET":
        return render(request,"logn/Student_template/result_view.html", {"result":True})
    if request.method == "POST":
        date=request.POST.get("date")
        date_parse=datetime.datetime.strptime(date,"%Y-%m-%d").date()
        course = Courses.objects.get(course_name=request.POST["course"])
        print(course.course_name, request.session["user"], ";")
        student=Students.objects.get(admin=request.user.id,date=date_parse)
        #student=Students.objects.get(dob=request.user.id)
        result=None
        print(student.id, "student this is")
        result_status=False
        message = ""
        try:
            result = Result.objects.filter(student_id=student, course_id = course)
            print(result)
        except Exception as e:
            result_status = True
            message = str(e)
          
    return render(request,"logn/Student_template/result_view.html", {"result":result_status,"message":message, "result_value": result })

"""def view_result(request):
    if request.method == "GET":
        return render(request,"logn/Student_template/result_view.html", {"result":True})
    if request.method == "POST":
        course = Courses.objects.get(course_name=request.POST["course"])
        print(course.course_name, request.session["user"], ";")
        student = Students.objects.get(id=request.session["user"])
        
        result=None
        print(student, "student this is")
       # print(student[0].first_name,"this is match")
        result_status=False
        message = ""
        try:
            result = Result.objects.filter(student_id=student.admin.id, course_id = course)
            print(result)
        except Exception as e:
            result_status = True
            message = str(e)
          
    return render(request,"logn/Student_template/result_view.html", {"result":result_status,"message":message, "result_value": result })"""

def std_changePass(request):
     if request.method=='POST':
         form = PasswordChangeForm(request.user,request.POST)
         if form.is_valid():
             form.save()
             messages.success(request,"Password Changes Successfullty")

     else:
         form = PasswordChangeForm(request.user)

     params={

        'form':form,
    }
     return render(request,'logn/Student_template/std_chnge_passwrd.html',params)

def fetch_stds(request, type_ac, course_id, year=None): 
    print(type_ac,course_id)
    if type_ac=="student":
        stu_obj=Courses.objects.get(id=course_id).students_set.ayearll()
        print(Courses.objects.get(id=course_id).students_set.all())
        data_variable=[]
        final_stu=[]
        if year:
            req_year = SessionYearModel.objects.get(id=year)
            print(req_year.session_start_year)
            for i in stu_obj:
                if req_year in i.session_year_id_set.all():
                    final_stu.append(i)
        else:
            final_stu=stu_obj
        print(final_stu)
        for i in final_stu:
            data_variable.append({"id":i.id, "first_name":i.admin.first_name, "last_name":i.admin.last_name})
    elif type_ac =="subject":
        cours=Courses.objects.get(id=course_id).subjects_set.all()
        print(Courses.objects.get(id=course_id).subjects_set.all())
        data_variable=[]
        for i in cours:
            data_variable.append({"id":i.pk, "first_name":i.subject_name, "last_name":""})
    else:
        data_variable=[]
    # data_variable=serializers.serialize(
    #                 'json', data_variable)
    print(data_variable)
    return HttpResponse(json.dumps(data_variable), content_type="application/json")

def fculty_give_notice_view(request):          
    print(request.user) 

    noticee=NoticeForStudentOnly.objects.filter(course_id=request.user.student.course_id)
    for n in noticee:
        print(n.seen)
        n.seen=True
        n.save()
    return render(request,"logn/Student_template/faculty_give_notice_view.html",{'noticee': noticee})
def sloogout(request):
    logout(request)
    return HttpResponseRedirect("/")