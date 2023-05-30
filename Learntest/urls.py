"""Learntest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
from app01.srcs.views import departments, myadmin, number, user, account, task, order

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("dbop", views.dbop),

    path("depart/list", departments.depart_list),
    path("depart/add", departments.depart_add),
    path("depart/<int:nid>/edit/", departments.depart_edit),
    path("depart/delete/", departments.depart_delete),

    path("user/list", user.user_list),
    path("user/add", user.user_add),
    path("user/delete/", user.user_delete),
    path("user/<nid>/edit/", user.user_edit),

    path("numbers/list", number.number_list),
    path("numbers/add", number.number_add),
    path("numbers/<int:nid>/edit", number.number_edit),
    path("numbers/delete/", number.number_delete),

    path("myadmin/list", myadmin.myadmin_list),
    path("myadmin/add", myadmin.myadmin_add),
    path("myadmin/<nid>/edit/", myadmin.myadmin_edit),
    path("myadmin/delete/", myadmin.myadmin_delete),
    path("myadmin/<nid>/reset/", myadmin.myadmin_reset_pwd),

    path("login/", account.login),
    path("logout/", account.logout),

    path("task/list", task.task_list),
    path("task/ajax", task.task_ajax),
    path("task/add", task.task_add),

    path("order/list", order.order_list)
]
