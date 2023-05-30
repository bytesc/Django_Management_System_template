
from django.shortcuts import render, redirect
from django import forms
from app01.models import Order


def order_list(request):
    content={}
    return render(request,"order/order_list.html",content)

