from django.contrib import messages 
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from logn.models import CustomUser , Courses ,Faculty ,Students,Subjects,Fee_Record,SessionYearModel,Department,FeedBackStudent,Fees,Contact,Fee_payment
from logn.models import Notice
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.core import serializers
import json
from django.contrib.auth import authenticate, logout
from django.db.models import Q


#ADMIN HOME PAGE
def homeadmin_template(request):
    student_count1=Students.objects.all().count()
    faculty_count=Faculty.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    



    return render(request,'logn/homeadmin_template.html',{"student_count":student_count1,"faculty_count":faculty_count,"subject_count":subject_count,"course_count":course_count})


#COURSE 
def add_course(request):
    return render(request,"logn/add_course.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect("logn/add_course")
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect("logn/add_course")


def courseview(request):
    course=Courses.objects.all()
    return render(request,"logn/courseview.html",{'course': course})

def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"logn/edit_course.html",{"course":course})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect("logn/edit_course/"+course_id)
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect("/edit_course/"+course_id)

def delete(request,course_id):
    course=Courses.objects.get(id=course_id)
    course.delete()
    return redirect("/courseview")



# admin add, delete, edit subject 
def add_sub(request):
    course=Courses.objects.all()
    faculty=CustomUser.objects.filter(user_type=2)
    return render(request,"logn/add_subject.html",{'course':course,'faculty':faculty})  

def add_sub_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        faculty_id=request.POST.get("faculty")
        faculty=CustomUser.objects.get(id=faculty_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course,faculty_id=faculty)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_sub"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_sub"))

def subject_view(request):
    subjects=Subjects.objects.all()
   
    return render(request,"logn/subject_view.html",{"subjects":subjects})

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    course=Courses.objects.all()
    faculty=CustomUser.objects.filter(user_type=2)
    return render(request,"logn/edit_subject.html",{"subject":subject,'course':course,'faculty':faculty})


def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        faculty_id=request.POST.get("faculty")
        course_id=request.POST.get("course")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            faculty=CustomUser.objects.get(id=faculty_id)
            subject.faculty_id=faculty
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))



def delete_subject(request,subject_id):    
  subjects=Subjects.objects.all()
  subjects.delete()
  return redirect("/subject_view")

     
#admin add student,edit ,delete
def add1(request):  
    #student=Students.objects.get(admin_id=request.user.id)
    #print("Email : "+student.admin.email)
    course=Courses.objects.all()
    sessionyear=SessionYearModel.object.all()
    return render(request,"logn/add1_student.html",{"course":course,'sessionyear':sessionyear})
    
def add1_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
    
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password") 
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
           
        try:
            user=CustomUser.objects.create_user( username=username , password=password, email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.student.address=address
            user.student.date=date
            user.student.phno=phno
            course_obj=Courses.objects.get(id=course_id)
            user.student.course_id=course_obj
            session_year=SessionYearModel.object.get(id=session_year_id)
            user.student.session_year_id=session_year
            user.student.gender=gender
            user.student.profile_pic=profile_pic_url
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect("add1")
        except:
            messages.error(request,"Failed to Add Student")
            return HttpResponseRedirect("logn/add1")

def student_view(request):
    student=Students.objects.all()
    return render(request,"logn/student_view.html",{'student': student})

def delete_student(request,student_id):
    student=Students.objects.get(id=student_id)
    student.delete()
    return redirect("/student_view")
    
def edit_student(request,student_id):
    course=Courses.objects.all()
    sessionyear=SessionYearModel.object.all()
    student=Students.objects.get(admin=student_id)
    return render(request,"logn/student_edit.html",{"student":student,"course":course,'sessionyear':sessionyear})

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

        
        #try:
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
        student.session_year_id = session_year
        student.gender=gender
        course=Courses.objects.get(id=course_id)
        student.course_id=course
            
        student.save()
        messages.success(request,"Successfully Edited Student")
        return HttpResponseRedirect("/edit_student/"+student_id)
      #  except:
          #  messages.error(request,"Failed to Edit Student")
           # return HttpResponseRedirect("/edit_student/"+student_id)

     
#admin gives notification in homepage for everyone
def noticeinsert(request):
    department=Department.objects.all()
    return render(request,"logn/noticeinsert.html",{'department':department})

def noticeinsert_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        subject=request.POST.get("subject")
        msg=request.POST.get("msg")
        try:
            notice_model=Notice(subject=subject,msg=msg)
            notice_model.save()
            messages.success(request,"Successfully Added Notification")
            return HttpResponseRedirect("logn/noticeinsert")
        except:
            messages.error(request,"Failed To Add Notification")
            return HttpResponseRedirect("logn/noticeinsert")


def viewnotification(request):
    notice=Notice.objects.all()
    return render(request,"logn/viewnotification.html",{'notice': notice})

def edit_notice(request,id):
    notice=Notice.objects.get(id=id)
    return render(request,'logn/edit_notice.html',{"notice":notice})

def edit_notice_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        id=request.POST.get("id")
        subject=request.POST.get("notice")
        msg=request.POST.get("notice")

        try:
                notice=Notice.objects.get(id=id)
                notice.subject=subject
                notice.msg=msg
                notice.save()
                messages.success(request,"Successfully Edited Notice")
                return HttpResponseRedirect("logn/edit_notice/"+id)
        except:
                messages.error(request,"Failed to Edit Staff")
                return HttpResponseRedirect("edit_notice/"+id)

def deletenotice(request,notice_id):
    notice=Notice.objects.get(id=notice_id)
    notice.delete()
    return redirect("/viewnotification")

# admin add staff,edit delete
def add_faculty(request):
    department=Department.objects.all()
    #return render(request,"logn/add_faculty.html",{'department':department})
    return render(request,"logn/facultyadd.html",{'department':department})


"""def add_faculty_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        email=request.POST.get("email")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
       
        password=request.POST.get("password")
        address=request.POST.get("address")
        department_id=request.POST.get("department")
        #try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
        user.faculty.address=address
        department_name=Department.objects.get(id=department_id)
       
        user.save()
        messages.success(request,"Successfully Added Faculty")
        return HttpResponseRedirect("/add_faculty")
        #except:
            #messages.error(request,"Failed to Add Faculty")
            #return HttpResponseRedirect("logn/add_faculty")"""



#delete if not work
def add_faculty_save(request): 
   if request.method!="POST":
        return HttpResponse("Method Not Allowed")
   else:    
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password")   
        email=request.POST.get("email")
        address=request.POST.get("address")
        department_id=request.POST.get("department")
        try:
       
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.faculty.address=address
            department_obj=Department.objects.get(id=department_id)
            user.faculty.department_id=department_obj
        
            user.save()
            messages.success(request,"Successfully Added Faculty")
            return HttpResponseRedirect("/add_faculty")
        except:
            messages.error(request,"Failed to Add Faculty")
            return HttpResponseRedirect("logn/add_faculty")


def view_staff(request):
    faculty=Faculty.objects.all()
    return render(request,"logn/view_staff.html",{'faculty': faculty})


def edit_faculty(request,faculty_id):
    faculty=Faculty.objects.get(admin=faculty_id)
    return render(request,"logn/edit_faculty.html",{"faculty":faculty})

def edit_faculty_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        
        faculty_id=request.POST.get("faculty_id")
        email=request.POST.get("email")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=faculty_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            faculty_model=Faculty.objects.get(admin=faculty_id)
            faculty_model.address=address
            faculty_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect("logn/edit_faculty/"+faculty_id)
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect("/edit_faculty/"+faculty_id)

def delete_faculty(request,faculty_id):
    faculty=Faculty.objects.get(id=faculty_id)
    faculty.delete()
    return redirect("/view_staff")

# admin add year 
def manage_session(request):
    return render(request,"logn/manage_session.html")

def add_session_save(request):
   if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
   else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))
#admin add department 
def add_dept(request):
    return render(request,"logn/add_dept.html")    
   

def add_dept_save(request): 
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        department=request.POST.get("department")
        try:
            department_model=Department(department_name=department)
            department_model.save()
            messages.success(request,"Successfully Added Department")
            return HttpResponseRedirect("logn/add_dept")
        except:
            messages.error(request,"Failed To Add")
            return HttpResponseRedirect("logn/add_dept")

def dept_view(request):
    department=Department.objects.all()
   
    return render(request,"logn/dept_view.html",{'department':department})

def dept_edit(request,department_id):
    department=Department.objects.get(id=department_id)
    return render(request,"logn/dept_edit.html",{"department":department})


def dept_edit_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        department_id=request.POST.get("department_id")
        department_name=request.POST.get("department")

        try:
            department=Department.objects.get(id=department_id)
            department.department_name=department_name
            department.save()
            messages.success(request,"Successfully Edited Department")
            return HttpResponseRedirect("logn/dept_edit/"+department_id)
        except:
            messages.error(request,"Failed to Edit Department")
            return HttpResponseRedirect("/dept_edit/"+department_id)

def delete_dept(request,department_id):
   department=Department.objects.get(id=department_id)
   department.delete()
   return redirect("/dept_view")
#admin view all the feedback that the student give to faculty
def feedbackview(request):
    feedback_data=FeedBackStudent.objects.all()
    return render(request,"logn/feedback_view.html",{'feedback_data':feedback_data})


    #amin can also reply to the feedback 

@csrf_exempt
def feedback_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    #try:
    feedback=FeedBackStudent.objects.get(id=feedback_id)
    feedback.feedback_reply=feedback_message
    feedback.save()
    return HttpResponse("True")
    #except:
        #return HttpResponse("False")    


#search student 
def search(request):
    student=Students.objects.all()
    params={'student':student}
   # query=request.GET.get('search')
  #  student=Students.objects.filter(title_icontains=query)
    return render(request,"logn/student_search.html",params)

"""def contact(request):

    return render(request,'logn/contact.html')

def contact_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name=request.POST.get("name") 
        email=request.POST.get("email") 
        comment=request.POST.get("comment") 
        try:
            contact_model=Contact(name=name,email=email,comment=comment)
            contact_model.save()
            messages.success(request,"Successfully Added Notification")
            return HttpResponseRedirect("logn/contact")
        except:
            messages.error(request,"Failed To Add Notification")
            return HttpResponseRedirect("logn/contact")"""



# can view the contact of people            
def contact_view(request):
    contact=Contact.objects.all()
    return render(request,"logn/contact_view.html",{'contact':contact})


#faculty view notification
def faculty_view_notice_list(request):

    notice_list=Notice.objects.all()
    return render(request,'logn/Faculty_template/notification_view.html',{'notice_list': notice_list})
# admin add fee of the course
def admin_set_fees(request):
    course=Courses.objects.all()
    return render(request,'logn/set_course_fee.html',{'course':course})

def admin_set_fees_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        tot_amount=request.POST.get("tot_amount")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
       

        try:
            fees=Fees(tot_amount=tot_amount,course_id=course)
            fees.save()
            messages.success(request,"Successfully Added ")
            return HttpResponseRedirect(reverse("admin_set_fees"))
        except:
            messages.error(request,"Failed ")
            return HttpResponseRedirect(reverse("admin_set_fees"))

def admin_set_fees_view(request):
    fees=Fees.objects.all()
    return render(request,"logn/course_fees_view.html",{'fees':fees})

def admin_set_fees_edit(request,fees_id):
    course=Courses.objects.all()
    fees=Fees.objects.get(id=fees_id)
    return render(request,"logn/admin_set_fees_edit.html",{'fees':fees,"course":course})



def admin_set_fees_edit_save(request):

    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        fees_id=request.POST.get("fees_id")
        tot_amount=request.POST.get("tot_amount")
        course_id = request.POST.get("course")
    

        try:
            fees=Fees.objects.get(id=fees_id)
            fees.tot_amount=tot_amount
            course=Courses.objects.get(id=course_id)
            fees.course_id=course
            fees.save()
            messages.success(request,"Successfully Added ")
            return HttpResponseRedirect(reverse("admin_set_fees/",kwargs={"fees_id":fees_id}))
        except:
            messages.error(request,"Failed to Add ")
            return HttpResponseRedirect(reverse("admin_set_fees/",kwargs={"fees_id":fees_id}))

def delete_course_fees(request,fees_id):
    fees=Fees.objects.get(id=fees_id)
    fees.delete()
    return redirect("/admin_set_fees_view")


def admin_notification_area(request):
    return render(request, "logn/not_aaa.html", {"notifications": Fee_payment.objects.all()})

#admin add fee that the student has paid 

def admin_insert_fees(request):
    course=Courses.objects.all()
    student=Students.objects.all()

    return render(request, "logn/fee_insert_record.html", {"course": course,"student":student})
def admin_fee_insert_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        
        course_id=request.POST.get("course")
        paid= request.POST.get("paid")
        pending=request.POST.get("pending")
        student_id=request.POST.get("student")
        amnt=request.POST.get("amnt")
        date = request.POST.get("date")
        course_obj=Courses.objects.get(id=course_id)
        # student_id=request.POST.get("student")
        print(student_id)
        student_obj=Students.objects.get(id=student_id)
        print(student_id)
       # p=Fee_Record(pending=int(amnt)-int(paid))
        #print(p)

        #try:
        fee_record=Fee_Record(amnt=amnt, date=date, course_id=course_obj,paid=paid,student_id=student_obj, pending=pending)
        fee_record.course_id=course_obj   
      #  print(Students.objects.get(id=request.session["user"]))
      #  fee_payment.student_id = Students.objects.get(id=request.session["user"])

        fee_record.save()
      #  print(fee_payment)
        messages.success(request,"Successfully Edited")
        return HttpResponseRedirect(reverse("admin_insert_fees"))
       # except:
          #  messages.error(request,"Failed to Edit Subject")
           # return HttpResponseRedirect(reverse("fee_payment"))



def admin_fee_payment(request): 
    course=Courses.objects.all()
    
    return render(request,"logn/Student_template/fee_payment.html",{'course':course})

def admin_fee_payment_save(request):
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
        messages.success(request,"Successfully Edited ")
        return HttpResponseRedirect(reverse("fee_payment"))
       # except:
          #  messages.error(request,"Failed to Edit Subject")
           # return HttpResponseRedirect(reverse("fee_payment"))


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

def view_fees_detail_student(request):
     fee_record=Fee_Record.objects.all()
  #   amnt=request.POST.get("amnt")
   #  paid= request.POST.get("paid")
    # p=request.GET.get(pending=amnt-paid)

     return render(request,"logn/student_detail_fees_view.html",{'fee_record':fee_record,})


def delete_fee_record(request,fe_id):
   fee_record=Fee_Record.objects.get(id=fe_id)
   fee_record.delete()
   return redirect("/view_fees_detail_student")

def edit_fees_detail_student(request,fe_id):   
    
    course=Courses.objects.all()
    student=Students.objects.all()

    fee_record=Fee_Record.objects.get(id=fe_id)
    return render(request,"logn/edit_fees_details_std.html",{'fee_record':fee_record,'course':course,"student":student})



def edit_fees_details_student_save(request):
     if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
     else:
        fe_id=request.POST.get("fe_id")
        amnt=request.POST.get("amnt")
        paid=request.POST.get("paid")
        pending=request.POST.get("pending")
        student_id=request.POST.get("student")
        course_id=request.POST.get("course")

       # try:
        fe_id=request.POST.get("id")
        fee_record=Fee_Record.objects.get(id=fe_id)
        fee_record.pending=pending
        fee_record.amnt=amnt
        fee_record.paid=paid
        student=Students.objects.get(id=student_id)
        fee_record.student_id=student
        course=Courses.objects.get(id=course_id)
        fee_record.course_id=course
        fee_record.save()

        messages.success(request,"Successfully Edited ")
        return HttpResponseRedirect("logn/view_fees_detail_student")
        #except:
           # messages.error(request,"Failed to Edit Subject")
            #return HttpResponseRedirect("logn/edit_fees_detail_student/"+fe_id)

def admin_changePass(request):
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
     return render(request,'logn/admin_chnge_passwrd.html',params)

def fetch_stds(request, type_ac,course_id): 
    print(type_ac,course_id)
    if type_ac=="student":
        cours=Courses.objects.get(id=course_id).students_set.all()
        print(Courses.objects.get(id=course_id).students_set.all())
        data_variable=[]
        for i in cours:
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

def slogout(request):
    logout(request)
    return HttpResponseRedirect("/")

def dep_search(request):
    search=request.GET.get('search')
    match=Department.objects.filter(Q(department_name__icontains=search))
    # print(match[0].first_name,"this is match")
    return render(request,'logn/Search_Dept.html',{'department':match})  

def course_search(request):
    search=request.GET.get('search')
    match=Courses.objects.filter(Q(course_name__icontains=search))
    return render(request,'logn/Search_Course.html',{'course':match})  

def fac_search(request):
    search=request.GET.get('search')
    match=CustomUser.objects.filter(Q(first_name__icontains=search))

    
    #stu_obj=Students.objects.get(match)
    #student=Students.objects.all()
   # print(match[0].first_name,"this is match")
    return render(request,'logn/Search_fac.html',{'faculty':match})    