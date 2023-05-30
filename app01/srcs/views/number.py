from django.shortcuts import render, redirect

from app01.models import Department, UserInfo, PhoneNumbers
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import NumModelForm, NumModelFormEdit, UserModelForm


def number_list(req):
    search_data_dict = {}
    search_data = req.GET.get("q", "")
    page = int(req.GET.get("page", "1"))  # 第二个参数表示默认数值
    start_page = page-5
    end_page = page+5

    if search_data:
        search_data_dict["mobile__contains"] = search_data
        # mobile__contains==xx 作为filter参数表示字符串包含xx 类似的 还有 __gt __lte __startwith
    queryset = PhoneNumbers.objects.filter(**search_data_dict).order_by("-level")
    # 相当于 order by level desc ,   queryset切片可以越界但要为正数

    page_nav_obj = PageNav(req, queryset)
    page_queryset = page_nav_obj.page_queryset
    page_nav_string = page_nav_obj.get_html()
    content = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_nav_string": page_nav_string,
    }
    return render(req, "numbers/num_list.html", content)


def number_add(req):
    if req.method == "GET":
        form = NumModelForm()
        content = {
            "form": form
        }
        return render(req, "numbers/num_add.html", content)
    form = NumModelForm(data=req.POST)
    if form.is_valid():
        # form.instance.字段名 = 手动赋值
        form.save()
        return redirect("/numbers/list")
    return render(req, "numbers/num_add.html", {"form": form})


def number_edit(req, nid):
    obj_row = PhoneNumbers.objects.filter(id=nid).first()
    if req.method == "GET":
        form = NumModelFormEdit(instance=obj_row)
        return render(req, "numbers/num_edit.html", {"form": form})
    form = NumModelFormEdit(instance=obj_row, data=req.POST)
    if form.is_valid():
        form.save()
        return redirect("/numbers/list")
    return render(req, "numbers/num_edit.html", {"form": form})


def number_delete(req):
    nid = req.GET.get("nid")
    PhoneNumbers.objects.filter(id=nid).delete()
    return redirect("/numbers/list")