from django.conf.urls.static import static
from finalpro import settings
from django.contrib import admin 
from django.urls import path
from logn import views, adminview,StudentView,FacultyView
from notice import views
from . import views
from  django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.home, name='home'),
    path("login",views.loginn, name="login"),
    path('loogout', views.loogout,name="loogout"),
    path("register",views.register, name="register"),
    path("contact",views.contact,name="contact"),
    path("contact_save",views.contact_save,name="contact_save"),
    path("contact_view",adminview.contact_view,name="contact_view"),
    path("about",views.about, name="about"),
    path("homeadmin_template",adminview.homeadmin_template, name="homeadmin_template"),
    path('add_course', adminview.add_course),
    path('add_sub', adminview.add_sub,name="add_sub"),
    path('add_sub_save', adminview.add_sub_save,name="add_sub_save"),
    path('subject_view', adminview.subject_view,name="subject_view"),
    path('edit_subject_save', adminview.edit_subject_save,name="edit_subject_save"),
    path('edit_subject/<str:subject_id>/', adminview.edit_subject,name="edit_subject"),
    path('delete_subject/<str:subject_id>/', adminview.delete_subject,name="delete_subject"),
    path('add_course_save', adminview.add_course_save),
    path('noticeinsert/', adminview.noticeinsert,name="noticeinsert"),
    path('noticeinsert_save', adminview.noticeinsert_save),
    path('edit_course/<str:course_id>/',  adminview.edit_course),
    path('edit_course_save', adminview.edit_course_save),
    path('courseview', adminview.courseview, name="courseview"),
    path('delete/<str:course_id>/', adminview.delete),
    path('edit_notice/<str:id>/',adminview.edit_notice),
    path('edit_notice_save',adminview.edit_notice_save),
   
    path('viewnotification', adminview.viewnotification),
    path('deletenotice/<str:notice_id>/', adminview.deletenotice),
    path('add_faculty', adminview.add_faculty),
    path('add_faculty_save', adminview.add_faculty_save),
    path('view_staff', adminview.view_staff, name="view_staff"),
    path('edit_faculty/<str:faculty_id>/',  adminview.edit_faculty),
    path('edit_faculty_save', adminview.edit_faculty_save),
    path('delete_faculty/<str:faculty_id>/', adminview.delete_faculty),
    path('manage_session', adminview.manage_session,name="manage_session"),
    path('add_session_save',adminview.add_session_save,name="add_session_save"),
    path('add_dept',adminview.add_dept, name="add_dept"),
    path('add_dept_save', adminview.add_dept_save, name="add_dept_save"),
    path('dept_view', adminview.dept_view, name="dept_view"),
    path('dept_edit/<str:department_id>/',adminview.dept_edit, name="dept_edit"),
    path('dept_edit_save',adminview.dept_edit_save, name="dept_edit_save"),
    path('delete_dept/<str:department_id>/',adminview.delete_dept, name="delete_dept"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="logn/passworddesign/password_reset_form.html"),name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="logn/passworddesign/password_reset_done.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="logn/passworddesign/password_reset_complete.html"),name="password_reset_complete"),
    path('feedbackview/',adminview.feedbackview,name="feedbackview"),
    path('feedback_replied/',adminview.feedback_replied,name="feedback_replied"),
    path('search/',adminview.search,name="search"),
    path('faculty_view_notice_list', adminview.faculty_view_notice_list ,name="faculty_view_notice_list"),
    path('admin_set_fees', adminview.admin_set_fees ,name="admin_set_fees"),
    path('admin_set_fees_view', adminview.admin_set_fees_view ,name="admin_set_view"),
    path('admin_set_fees_save', adminview.admin_set_fees_save ,name="admin_set_fees_save"),
    path('delete_course_fees/<str:fees_id>', adminview.delete_course_fees ,name="delete_course_fees"),
    path("admin_notification", adminview.admin_notification_area, name="admin_notification"),
    path("admin_insert_fees", adminview.admin_insert_fees, name="admin_insert_fees"),
    path("admin_fee_insert_save", adminview.admin_fee_insert_save, name="admin_fee_insert_save"),
    path('admin_set_fees_edit/<str:fees_id>/', adminview.admin_set_fees_edit, name="admin_set_fees_edit"),
    path('admin_set_fees_edit_save', adminview.admin_set_fees_edit, name="admin_set_fees_edit_save"),
    path('view_fees_detail_student', adminview. view_fees_detail_student, name="view_fees_detail_student"),
    path('delete_fee_record/<str:fe_id>/',adminview.delete_fee_record, name="delete_fee_record"),
    path('edit_fees_detail_student/<int:fe_id>/',adminview.edit_fees_detail_student,name="edit_fees_detail_student"),
    path('edit_fees_details_student_save',adminview.edit_fees_details_student_save,name="edit_fees_details_student_save"),
    path('admin_changePass',adminview.admin_changePass,name="admin_changePass"),
    path('admin_fee_payment', adminview.admin_fee_payment,name="admin_fee_payment"),
    path('admin_fee_payment_save', adminview.admin_fee_payment_save,name="admin_fee_payment_save"),
    path('student_view', adminview.student_view, name="student_view"),
    path('slogout', adminview.slogout, name="slogout"),
    path('dep_search', adminview.dep_search, name="dep_search"),
    path('course_search', adminview.course_search, name="course_search"),
    path('fac_search', adminview.fac_search, name="fac_search"),






    # Student URL PATH
    path('student_home', StudentView.student_home ,name="student_home"),
    path('fetch_std/<type_ac>/<course_id>',adminview.fetch_stds, name="fetch_std"),
    
   
   
    path('add1', adminview.add1, name="add1"),
    path('add1_save', adminview.add1_save,name="add1_save"),
    path('edit_student/<str:student_id>/',adminview.edit_student,name="edit_student"),
    path('edit_student_save',adminview.edit_student_save,name="edit_student_save"),
    path('delete_student/<str:student_id>/',adminview.delete_student,name="delete_student"),
    path('give_feedback', StudentView.give_feedback,name="give_feedback"),
    path('student_view_attendance', StudentView.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentView.student_view_attendance_post, name="student_view_attendance_post"),
    # delete this too
    path('fetch_dep/<department_id>', StudentView.fetch_api, name="fetch_dep"),

    path('give_notice_view',StudentView.fculty_give_notice_view ,name="give_notice_view"),


    path('feedback_save', StudentView.feedback_save,name="feedback_save"),
    path('course_fetch/<course_id>', adminview.course_fetch, name="course_fetch"),
    path('fee_payment', StudentView.fee_payment,name="fee_payment"),
    path('fee_payment_save', StudentView.fee_payment_save,name="fee_payment_save"),
    path('pay', StudentView.pay,name="pay"),
    path("view_result", StudentView.view_result, name="view_result"),
    path("std_changePass", StudentView.std_changePass, name="std_changePass"),
    path("sloogout", StudentView.sloogout, name="sloogout"),
   

    # Faculty URL PATH
    path('faculty_home', FacultyView.faculty_home ,name="faculty_home"),
    path('result', FacultyView.result,name="result"),
    path('result_view', FacultyView.result_view,name="result_view"),
    path('result_save', FacultyView.result_save,name="result_save"),
    path('result_edit/<str:result_id>/',FacultyView.result_edit,name="result_edit"),
    path('result_edit_save', FacultyView.result_edit_save,name="result_edit_save"),
    path('delete_result/<str:result_id>/',FacultyView.delete_result,name="delete_result"),
    path('take_attendance', FacultyView.take_attendance,name="take_attendance"),
    path('faculty_update_attendance', FacultyView.faculty_update_attendance,name="faculty_update_attendance"),
    path('get_attendance_dates', FacultyView.get_attendance_dates,name="get_attendance_dates"),
    path('get_attendance_student', FacultyView.get_attendance_student, name="get_attendance_student"),
    path('get_students', FacultyView.get_students, name="get_students"),
    path('save_attendance_data', FacultyView.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data',FacultyView.save_updateattendance_data, name="save_updateattendance_data"),
    path('floogout/', FacultyView.floogout, name="floogout"),
    path('faculty_give_notice', FacultyView.faculty_give_notice ,name="faculty_give_notice"),
    path('faculty_give_notice_save', FacultyView.faculty_give_notice_save ,name="faculty_give_notice_save"),
    path('faculty_give_notice_view', FacultyView.faculty_give_notice_view ,name="faculty_give_notice_view"),
    path('delete_notification/<nid>', FacultyView.Delete_notification, name="delete_notification"),
  #  path('faculty_view_notice_list', adminview.faculty_view_notice_list ,name="faculty_view_notice_list"),
    path('fac_changePass', FacultyView.fac_changePass,name="fac_changePass"), 
    path('f_student_view', FacultyView.f_student_view, name="f_student_view"),
   
    path('f_courseview', FacultyView.f_courseview),
    path('fetch_stdd/<type_ac>/<course_id>',FacultyView.fetch_stdd, name="fetch_stdd"),
    path('fetch_stdd/<type_ac>/<course_id>/<year>',FacultyView.fetch_stdd, name="fetch_stdd"),



   

   
    
    
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
