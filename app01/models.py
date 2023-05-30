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

    def __str__(self):
        return self.name


class PhoneNumbers(models.Model):
    mobile = models.CharField(verbose_name="手机号", max_length=11, null=True, blank=True)
    price = models.DecimalField(verbose_name="价格", decimal_places=2, max_digits=10, null=True, blank=True)
    level_choices = (
        (1, "一级"),
        (2, "二级别"),
        (3, "三级别"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1, null=True, blank=True)
    status_choices = (
        (1, "占用"),
        (2, "未占用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2, null=True, blank=True)


class MyAdmin(models.Model):
    id = models.CharField(verbose_name="管理员账号", primary_key=True, max_length=32)
    user_name = models.CharField(verbose_name="管理员名", max_length=32)
    password = models.CharField(verbose_name="管理员密码", max_length=64)

    class Meta:
        verbose_name = "管理员"
        db_table = "管理员表"

    def __str__(self):
        return self.user_name


class Task(models.Model):
    title = models.CharField(verbose_name="标题", max_length=64)
    level_choices = (
        (1, "紧急"),
        (2, "一般"),
        (3, "不紧急"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=2)
    user = models.ForeignKey(verbose_name="负责人", to="MyAdmin", to_field="id", null=True, blank=True,
                             on_delete=models.SET_NULL)
    detail = models.TextField(verbose_name="详细信息", null=True, blank=True)


class Order(models.Model):
    oid = models.CharField(verbose_name="订单号", max_length=64, primary_key=True)
    title = models.CharField(verbose_name="名称", max_length=32, blank=True,null=True)
    price = models.DecimalField(verbose_name="价格",blank=True,null=True,decimal_places=2,max_digits=10)
    status_choices= (
        (1,"待支付"),
        (2,"支付中"),
        (3,"已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,blank=True,null=True)
    admin = models.ForeignKey(verbose_name="管理员",to="MyAdmin",to_field="id",
                              null=True,blank=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(verbose_name="用户",to="UserInfo",to_field="user_id",
                             null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

