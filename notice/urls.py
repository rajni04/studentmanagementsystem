from django.urls import path
from django.contrib import admin
from django.urls.conf import include
from notice import views
from logn import adminview
from django.views.generic.base import RedirectView



urlpatterns = [
    path('notice_list/', views.notice_list,name="notice_list"),
    path('notice_list_detail/<str:id>/', views.notice_list_detail,name="notice_list_detail"),
    path('', RedirectView.as_view(url="notice/")) , 
    path('noticeinsert', views.noticeinsert, name="noticeinsert"), 
    path('edit_notice/<str:id>/',adminview.edit_notice),
    path('edit_notice_save',adminview.edit_notice_save),
   # path('notice_list/<int:pk>', views.NoticeDetailView.as_view()),
    
   
   
]
