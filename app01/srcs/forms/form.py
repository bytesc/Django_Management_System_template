from django import forms
from app01.utils.bootstrap_modelform import BootstrapModelForm
from app01.models import *

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UserModelForm(BootstrapModelForm):
    age = forms.IntegerField(required=False,
                             widget=forms.TextInput(attrs={"class": "form-control", "type":"number", "placeholder": "年龄", "min": "0", "max": "135"}))
    creat_time = forms.DateTimeField(required=False,
                                 widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    class Meta:  # 这里必须是Meta四个字母，不能错
        model = UserInfo  # 这里必须是model字母，不能错
        fields = ["user_id", "name", "password", "account", "age", "creat_time", "gender", "department"]  # 这里必须是fields字母，不能错
        # widgets = {
        #     "department": forms.TextInput(attrs={"class": "form-control"})
        # }


class NumModelForm(BootstrapModelForm):
    class Meta:
        model = PhoneNumbers  # 这里必须是model字母，不能错
        fields = "__all__"  # 这里必须是fields字母，不能错
        # exclude = ["mobile"]

    # 验证方式3
    # clean_列名
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # 以下两条会报错
        # id = self.cleaned_data["price"]
        # id = self.cleaned_data["id"]
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        if PhoneNumbers.objects.filter(mobile=txt_mobile).exists():
            raise ValidationError("手机号已经存在")
        return txt_mobile

    # 验证方式4
    # mobile = forms.CharField(validators=[RegexValidator("^1[3-9]\d{9}$"),"格式错误"]
    #                         ,label="手机号", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class NumModelFormEdit(BootstrapModelForm):
    mobile = forms.CharField(disabled=True,  # disable输入框，使得不能编辑
                             label="手机号", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "手机号"}))

    class Meta:
        model = PhoneNumbers  # 这里必须是model字母，不能错
        fields = "__all__"  # 这里必须是fields字母，不能错
        # exclude = ["mobile"]

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        id = self.instance.pk
        # 以下两条会报错
        # id = self.cleaned_data["price"]
        # id = self.cleaned_data["id"]
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        # 编辑时排除自身
        if PhoneNumbers.objects.filter(mobile=txt_mobile).exclude(id=id).exists():
            raise ValidationError("手机号已经存在")
        return txt_mobile


from app01.utils.md5 import get_md5
class MyadminForm(BootstrapModelForm):
    user_name = forms.CharField(required=False, label="管理员姓名",
                                widget=forms.TextInput(attrs={"class": "form-control", }))
    password = forms.CharField(required=True, label="输入密码", min_length=8,
                                  widget=forms.PasswordInput(attrs={"class": "form-control", }))
    confirm_pwd = forms.CharField(required=True, label="确认密码", min_length=8,
                                widget=forms.PasswordInput(attrs={"class": "form-control", }))
    class Meta:
        model = MyAdmin  # 这里必须是model字母，不能错
        fields = "__all__"  # 这里必须是fields字母，不能错
        # exclude = ["mobile"]

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get("password")
        c_pwd = get_md5(self.cleaned_data.get("confirm_pwd"))
        if pwd != c_pwd:
            raise ValidationError("密码不一致")
        # 返回什么数据库里存什么
        return c_pwd

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 返回什么数据库里存什么
        return get_md5(pwd)


class MyadminFormEdit(BootstrapModelForm):
    class Meta:
        model = MyAdmin  # 这里必须是model字母，不能错
        fields = ["user_name"]  # 这里必须是fields字母，不能错


class MyadminFormReset(BootstrapModelForm):
    password = forms.CharField(required=True, label="输入密码", min_length=8,
                               widget=forms.PasswordInput(attrs={"class": "form-control", }))
    confirm_pwd = forms.CharField(required=True, label="确认密码", min_length=8,
                                  widget=forms.PasswordInput(attrs={"class": "form-control", }))
    class Meta:
        model = MyAdmin  # 这里必须是model字母，不能错
        fields = ["password","confirm_pwd"]  # 这里必须是fields字母，不能错
    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get("password")
        c_pwd = get_md5(self.cleaned_data.get("confirm_pwd"))
        if pwd != c_pwd:
            raise ValidationError("密码不一致")
        # 返回什么数据库里存什么
        return c_pwd

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 返回什么数据库里存什么
        return get_md5(pwd)

