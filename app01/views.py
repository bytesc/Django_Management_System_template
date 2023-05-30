from django.shortcuts import render, redirect, HttpResponse


# Create your views here.

def index(req):
    return render(req, "index.html")


def dbop(req):
    import random
    from app01.models import UserInfo, PhoneNumbers
    for i in range(100, 300):
            number = random.randint(1000000000, 9999999999)
            UserInfo.objects.create(user_id=str(i))
            PhoneNumbers.objects.create(mobile=number)
    return HttpResponse("done")









