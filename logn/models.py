from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    object=models.Manager()

class CustomUser(AbstractUser):
    user_type_data=((1,"ADMIN"),(2,"FACULTY"),(3,"STUDENT"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    first_name=models.CharField(max_length=10, validators=[alphanumeric])
    last_name=models.CharField(max_length=10)
    email=models.EmailField(max_length=20)
   

class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Department(models.Model):
    id=models.AutoField(primary_key=True)
    department_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
   


class Faculty(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField(max_length=50)
    department_id=models.ForeignKey(Department,on_delete=models.DO_NOTHING,default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE, related_name="student")
    date=models.DateField()
    phno=models.CharField(max_length=12)
    gender=models.CharField(max_length=10)
    profile_pic=models.ImageField()
    address=models.TextField(max_length=50)
    course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING,default=1)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=20)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    faculty_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField(max_length=50)
    feedback_reply = models.TextField(max_length=20)
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    faculty_id=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Result(models.Model):
    id=models.AutoField(primary_key=True)
    marksobtained=models.IntegerField()
    passmarks=models.IntegerField()
    totalmarks=models.CharField(max_length=3)
    assignment_marks=models.CharField(max_length=3,default=1)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=20)
    comment=models.CharField(max_length=30)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class NoticeForStudentOnly(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True)
    course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING,default=1)
    message=models.CharField(max_length=500)
    seen = models.BooleanField(default=False, null=True)
    objects=models.Manager()



class Notice(models.Model):
    subject=models.CharField(max_length=50)
    msg=models.TextField()
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    cr_date=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Fees(models.Model):
    tot_amount=models.PositiveIntegerField(null=True)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    objects=models.Manager()


class Fee_payment(models.Model):
    fees_id=models.ForeignKey(Fees,on_delete=models.DO_NOTHING,default=1)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    amount=models.PositiveIntegerField(null=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    date=models.DateField(auto_now=True)
    objects=models.Manager()

class Fee_Record(models.Model):
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    amnt=models.PositiveIntegerField(null=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    paid=models.PositiveIntegerField(null=True)
    pending=models.PositiveIntegerField(null=True)
    date=models.DateField(auto_now=True)
    objects=models.Manager()
    
    
@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(admin=instance)
        if instance.user_type==2:
            Faculty.objects.create(admin=instance,address="",department_id=Department.objects.get(id=1))
        if instance.user_type==3:
            Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),phno="",date="2020-01-01",session_year_id=SessionYearModel.object.get(id=1),address="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.faculty.save()
    if instance.user_type==3:
        instance.student.save()
