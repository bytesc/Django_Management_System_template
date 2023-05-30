from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django import forms
from app01.utils.md5 import get_md5
from app01.models import MyAdmin


# 用form自定义，也可以用modelform
class LoginForm(forms.Form):
    user_name = forms.CharField(label="用户名", required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"},))
    password = forms.CharField(label="密码", required=True,
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"},
                                                          render_value=True))  # render_value代表刷新不清空
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return get_md5(pwd)


def login(req):
    if req.method == "GET":
        form = LoginForm
        return render(req, "account/login.html", {"form": form})

    form = LoginForm(data=req.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # adm_obj = MyAdmin.objects.filter(user_name=form.cleaned_data.get("username"),
        #                        password=form.cleaned_data.get("password")).first()
        adm_obj = MyAdmin.objects.filter(**form.cleaned_data).first()
        if not adm_obj:
            form.add_error("password", "用户名或密码错误")
            return render(req, "account/login.html", {"form": form})
        req.session["info"] = {"id": adm_obj.id, "name": adm_obj.user_name}
        # return HttpResponse("提交成功")
        return redirect("/myadmin/list")
    return render(req, "account/login.html", {"form": form})


def logout(req):
    req.session.clear()
    return redirect("/")
