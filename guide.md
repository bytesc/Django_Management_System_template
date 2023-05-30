# Django4
## 基本配置
安装django，创建项目
```bash
pip install django
django-admin startproject Helloworld
```
创建app
```bash
python manage.py startapp app01
```
注册app，在settings.py中
```python
INSTALLED_APPS = [
    ...
    "app01.apps.App01Config",
    # 新建app要注册
]
```
配置静态文件（js,css）
```python
STATIC_URL = "static/"
```
配置模板（html）
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

## 数据库
安装mysqlclient
```bash
pip install mysqlclient
```
去手动创建数据库（mysql）
```bash
mysql -h192.168.5.116 -P3306 -uroot -p123456
mysql> show databases;
mysql> create database test;
```
配置数据库连接，在settings.py中
```python
# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
```python
# sqlite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```
在models.py中新建表
```python
from django.db import models
# Create your models here.
import datetime

class Department(models.Model):
    """部门表"""
    department_id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name="部门名", max_length=100, null=True, blank=True, default="")

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """用户表"""
    user_id = models.CharField(verbose_name="用户账号", primary_key=True, max_length=30)
    name = models.CharField(verbose_name="姓名", max_length=30, null=True, blank=True, default="")
    password = models.CharField(verbose_name="密码", max_length=64, null=True, blank=True, default="")
    age = models.IntegerField(verbose_name="年龄", null=True, blank=True, default=18)
    account = models.DecimalField(verbose_name="账户余额", decimal_places=2, max_digits=10, null=True, blank=True, default=0.0)
    # obj.creat_time.strftime("%Y-%m-%d")
    creat_time = models.DateTimeField(verbose_name="入职时间", null=True, blank=True, default=datetime.datetime.now())
    # django约束
    gender_choices = ((1, "男"), (2, "女"))
    # obj.get_gender_display()获取男女
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True, blank=True)
    # 数据库外键约束
    # Department.user_set()即可获取部门的所有员工
    department = models.ForeignKey(to="Department", to_field="department_id", related_name="user_set",
                                   verbose_name="所属部门", null=True, blank=True, on_delete=models.SET_NULL)
# on_delete=models.CASCADE 级联删除
```
用models.py更新数据库设计
```bash
python manage.py makemigrations
python manage.py migrate
```
## 项目结构和重要组件
- 在 urls.py 中，路由（URL 与 函数的对应关系）
- 在 views.py 中， 视图函数，编写业务逻辑
- templates目录，编写html（包括模板语法 {% static xxx %} ）
- ModelForm 和 Form 组件，在增删改查功能中
    - 生成 html 标签
    - 请求数据校验。
    - 保存到数据库 （ModelForm.save）
    - 获取错误信息
- Cookie 和 Session 保存用户登录信息
- 重写中间件的process_request函数实现用户认证
- ORM数据库操作（filter，orderby等）
- 分页组件 

## ajax
用type用button，id标签绑定事件，而不是用type="submit"
```html
<button id="btnAdd" type="button" class="btn btn-primary">提交</button>
```
```html
<script type="text/javascript">
        $(function () {
            //页面框架加载后自动执行
            bindBtnAddEvent();
        })
        function bindBtnAddEvent(){
             $("#btnAdd").click(function (){
                $(".error-msg").empty();
                 //先把错误信息置空
                $.ajax({
                url:"/task/add",
                type:"post",
                data:$("#formAdd").serialize(),
                    dataType:"JSON", //把json字符串转为前端js对象
                success: function (res){
                    console.log(res);
                    if(res.status){
                        alert("添加成功");
                    }
                    else {
                        // alert("添加失败");
                        // 循环每一个错误
                        $.each(res.error,function (name,data){
                            $("#id_" + name).next().text(data[0]);
                            // modelform自动生成的input框id属性，就是id_+字段名
                            // .next()表示下一个标签，.text()设置内容
                        })
                    }
                }
            })
            })
        }
</script>
```
view函数中需要免除csrf_token
```python
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt # 免除csrf_token认证，就可发post
```