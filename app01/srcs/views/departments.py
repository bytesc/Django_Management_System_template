from django.shortcuts import render, redirect

from app01.models import Department, UserInfo, PhoneNumbers
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import NumModelForm, NumModelFormEdit, UserModelForm


def depart_list(request):
    queryset = Department.objects.all()
    content = {
        "queryset": queryset,
    }
    return render(request, "departments/depart_list.html", content)


def depart_add(request):
    if request.method == "GET":
        return render(request, "departments/depart_add.html", )
    else:
        new_title = request.POST.get("new_title")
        Department.objects.create(title=new_title)
        return redirect("/depart/list")


def depart_delete(req):
    nid = req.GET.get("nid")
    Department.objects.filter(department_id=nid).delete()
    return redirect("/depart/list")


def depart_edit(req, nid):
    obj = Department.objects.filter(department_id=nid)
    if req.method == "GET":
        content = {
            "department_id": obj.first().department_id,
            "title": obj.first().title
        }
        return render(req, "departments/depart_edit.html", content)
    else:
        new_title = req.POST.get("new_title")
        obj.update(title=new_title)
        return redirect("/depart/list")