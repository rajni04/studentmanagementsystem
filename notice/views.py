from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from logn.models import Notice
from logn.models import Department
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

 
"""class NoticeDetailView(DetailView):
    model=Notice  """  

def noticeinsert(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        notice=request.POST.get("notice")
        try:
            department_id=request.POST.get("department")
            department=Department.objects.get(id=department_id)
            notice_model=Notice(subject=subject,msg=msg,department_id=department)
            notice_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect("/noticeinsert")
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect("/noticeinsert")

def edit_notice(request,notice_id):
    notice=Notice.objects.get(id=notice_id)
    return render(request,'logn/edit_notice.html',{"notice":notice})

def edit_notice_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        notice_id=request.POST.get("notice_id")
        subject=request.POST.get("notice")
        msg=request.POST.get("notice")

        try:
                notice=Notice.objects.get(id=notice_id)
                notice.subject=subject
                notice.msg=msg
                notice.save()
                messages.success(request,"Successfully Edited Notice")
                return HttpResponseRedirect("logn/edit_notice/"+notice_id)
        except:
                messages.error(request,"Failed to Edit Notice")
                return HttpResponseRedirect("/edit_notice/"+notice_id)

def notice_list(request):
    notice_list=Notice.objects.all()
    return render(request,'notice/notice_list.html',{'notice_list': notice_list})

def notice_list_detail(request,id):
    notice=Notice.objects.get(id=id)
    return render(request,'notice/notice_detail.html',{'notice':notice})





