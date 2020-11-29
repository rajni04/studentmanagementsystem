import json
from django.contrib.auth import authenticate, logout
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from logn.models import Result,Courses,CustomUser,Subjects,Students,SessionYearModel,Attendance,Faculty,AttendanceReport,NoticeForStudentOnly
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm




def faculty_home(request):
#For Fetch All Student Under Staff                                
    subjects=Subjects.objects.filter(faculty_id=request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()
#Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()
    subject_count=subjects.count()

    
    return render(request,"logn/Faculty_template/homefaculty_template.html",{"students_count":students_count,"attendance_count":attendance_count,"subject_count":subject_count})



def add(request):
    return render(request,"logn/Faculty_template/add.html")

#fetch student from coursesurls





def result(request):
    course=Courses.objects.all()
    subjects=Subjects.objects.all()
    student=Students.objects.all()
    
    sessionyear=SessionYearModel.object.all()
    return render(request,"logn/Faculty_template/result.html",{"course":course,'student':student,"subjects":subjects,'sessionyear':sessionyear})

def result_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
         subject_id=request.POST.get("subject")
         subject=Subjects.objects.get(id=subject_id)
         course_id=request.POST.get("course")
         course=Courses.objects.get(id=course_id)
         student_id=request.POST.get("student")
         
         student_obj=Students.objects.get(id=student_id)
         session_year_id=request.POST.get("session_year_id")
         session_year_id=SessionYearModel.object.get(id=session_year_id)
         marksobtained=request.POST.get("marksobtained")
         assignment_marks=request.POST.get("assignment_marks")
         passmarks=request.POST.get("passmarks")
         totalmarks=request.POST.get("totalmarks")
    #try:
         results=Result(marksobtained=marksobtained,passmarks=passmarks,totalmarks=totalmarks,assignment_marks=assignment_marks,subject_id=subject,course_id=course,student_id=student_obj,session_year_id=session_year_id)
         results.save()
         messages.success(request,"Successfully Added ")
         return HttpResponseRedirect(reverse("result"))
   # except:
        # messages.error(request,"Failed to Add Subject")
        # return HttpResponseRedirect(reverse("result"))

def result_view(request):  
    results=Result.objects.all()
    return render(request,"logn/Faculty_template/result_view.html",{'results': results})

def result_edit(request,result_id):
    result=Result.objects.get(id=result_id)
    subjects=Subjects.objects.all()
    course=Courses.objects.all()
    sessionyear=SessionYearModel.object.all()
    students=Students.objects.all()
    return render(request,"logn/Faculty_template/edit_result1.html",{"result":result,'student':students,'course':course,'sessionyear':sessionyear,'subjects':subjects})

def result_edit_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        result_id=request.POST.get("result_id")
        marksobtained=request.POST.get("marksobtained")
        assignment_marks=request.POST.get("assignment_marks") 
        passmarks=request.POST.get("passmarks")
        totalmarks=request.POST.get("totalmarks")

       # subject_id=request.POST.get("subject_id")
    
        #student_id=request.POST.get("student")
       # course_id=request.POST.get("course")

      #  try:
        result_id=request.POST.get("id")
        result=Result.objects.get(id=result_id)
        result.marksobtained=marksobtained
        result.assignment_marks=assignment_marks
        result.passmarks=passmarks
        result.totalmarks=totalmarks
       # student=CustomUser.objects.get(id=student_id)
        #result.student_id=student
        #course=Courses.objects.get(id=course_id)
        #result.course_id=course
        #subject=Subjects.objects.get(id=subject_id)
       # result.subject_id=subject
        result.save()

        messages.success(request,"Successfully Edited Subject")
        return HttpResponseRedirect(reverse("result_edit",kwargs={"result_id": result_id}))
        #except:
            #messages.error(request,"Failed to Edit Subject")
            #return HttpResponseRedirect(reverse("result_edit",kwargs={"result_id": result_id}))

def delete_result(request,result_id):    
  result=Result.objects.get(id=result_id)
  result.delete()
  return redirect("/result_view")





def take_attendance(request):
    subjects=Subjects.objects.filter(faculty_id=request.user.id)
    #subjects=Subjects.objects.all()
    session_years=SessionYearModel.object.all()
    return render(request,"logn/Faculty_template/attendance1.html",{"subjects":subjects,"session_years":session_years})


"""def staff_feedback(request):
    staff_id=Staffs.objects.get(admin=request.user.id)
    feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))    """


@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)
   
"""@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")"""

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

    
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
 


def faculty_update_attendance(request):
    subjects=Subjects.objects.filter(faculty_id=request.user.id)
    session_year_id=SessionYearModel.object.all()
    return render(request,"logn/Faculty_template/faculty_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})
    
@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")
        
def floogout(request):
    logout(request)
    return HttpResponseRedirect("/")

"""def teacher_notice_view(request):
    form=for*-ms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'school/teacher_notice.html',{'form':form})"""

def faculty_give_notice(request):
    course=Courses.objects.all()
    return render(request,"logn/Faculty_template/faculty_give_notice.html",{'course':course})

def faculty_give_notice_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course_id=request.POST.get("course")
        
        message=request.POST.get("message")
        by=request.user.first_name  #adding the faculty name in by
       
      #  try:
            
        noticee=NoticeForStudentOnly(message=message,by=by)
        course_obj=Courses.objects.get(id=course_id)
        noticee.course_id=course_obj
        noticee.save()
        messages.success(request,"Successfully Added Notification")
        return HttpResponseRedirect(reverse("faculty_give_notice"))
    
       # except:
          #  messages.error(request,"Failed To Add Notification")
         #   return HttpResponseRedirect(reverse("faculty_give_no   tice"))

def faculty_give_notice_view(request):          
    print(request.user) 

    noticee=NoticeForStudentOnly.objects.filter(course_id=request.user.student.course_id)
    for n in noticee:
        print(n.seen)
        n.seen=True
        n.save()
    return render(request,"logn/Student_template/faculty_give_notice_view.html",{'noticee': noticee})

def Delete_notification(request, nid):
    try:
        NoticeForStudentOnly.objects.get(id=nid).delete()
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps({}), content_type="application/json")

def f_student_view(request):
    student=Students.objects.all()
    return render(request,"logn/Faculty_template/student_record.html",{'student': student})


def fac_changePass(request):
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
     return render(request,'logn/Faculty_template/fac_chnge_passwrd.html',params)

def f_courseview(request):
    course=Courses.objects.all()
    return render(request,"logn/Faculty_template/course_view.html",{'course': course})





def fetch_stdd(request, type_ac, course_id, year=None): 
    print(type_ac,course_id)
    if type_ac=="student":
        stu_obj=Courses.objects.get(id=course_id).students_set.all()
        # print(Courses.objects.get(id=course_id).students_set.all())
        data_variable=[]
        final_stu=[]
        if year:
            req_year = SessionYearModel.object.get(id=year)
            print(req_year.session_start_year,req_year.students_set.all(),"thiisis thsbdiuab")
            for i in stu_obj:
                if req_year == i.session_year_id:
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