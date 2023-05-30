from django.shortcuts import render, redirect

from app01.models import Department, UserInfo, PhoneNumbers, MyAdmin
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import  MyadminForm, MyadminFormEdit ,MyadminFormReset


def myadmin_list(req):
    info = req.session.get("info")
    # 获取session信息，未登录则去登录
    if not info:
        return redirect("/login/")

    search_data_dict = {}
    search_data = req.GET.get("q", "")

    if search_data:
        search_data_dict["user_name__contains"] = search_data
        # mobile__contains==xx 作为filter参数表示字符串包含xx 类似的 还有 __gt __lte __startwith
    queryset = MyAdmin.objects.filter(**search_data_dict)
    # 相当于 order by level desc ,   queryset切片可以越界但要为正数

    # queryset = UserInfo.objects.all()
    page_nav_obj = PageNav(req, queryset)
    page_queryset = page_nav_obj.page_queryset
    page_nav_string = page_nav_obj.get_html()
    content = {
        "queryset": page_queryset,
        "page_nav_string": page_nav_string,
    }
    return render(req, "myadmin/myadmin_list.html", content)


def myadmin_add(req):
    if req.method == "GET":
        form = MyadminForm()
        return render(req, "change.html", {"form": form, "add_name": "添加管理员"})
    else:
        form = MyadminForm(data=req.POST)  # 用post的消息更新表单，没有instance表示新增而不是修改
        if form.is_valid():
            # print(form.cleaned_data)
            # 自定义函数验证form.cleaned_data["password"] raise forms.ValidationError('密码不构长', code='invalid mobile')
            form.save()
            return redirect("/myadmin/list")
        else:
            # print(form.errors)
            return render(req, "change.html", {"form": form, "title": "添加管理员"})


def myadmin_delete(req):
    nid = req.GET.get("nid")
    MyAdmin.objects.filter(id=nid).delete()
    return redirect("/myadmin/list")


def myadmin_edit(req, nid):
    row_obj = MyAdmin.objects.filter(id=nid).first()
    if not row_obj:
        return render(req, "error.html")

    if req.method == "GET":
        form = MyadminFormEdit(instance=row_obj)
        return render(req, "change.html", {"form": form, "title": "编辑管理员"})
    else:
        form = MyadminFormEdit(instance=row_obj, data=req.POST)
        if form.is_valid():
            form.save()
            return redirect("/myadmin/list")
        return render(req, "change.html", {"form": form, "title": "编辑管理员"})


def myadmin_reset_pwd(req, nid):
    row_obj = MyAdmin.objects.filter(id=nid).first()
    if not row_obj:
        return render(req, "error.html")

    if req.method == "GET":
        form = MyadminFormReset(instance=row_obj)
        return render(req, "change.html", {"form": form, "title": "重置密码"})
    else:
        form = MyadminFormReset(instance=row_obj, data=req.POST)
        if form.is_valid():
            form.save()
            return redirect("/myadmin/list")
        return render(req, "change.html", {"form": form, "title": "重置密码"})
