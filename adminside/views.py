from django.shortcuts import render,redirect
from django.http import HttpResponse
from user.models import *
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.http import FileResponse
import os
from django.conf import settings
from datetime import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def states(request):
    if request.POST.get("btnStateInsert"):
        s=state()
        s.statename=request.POST.get("txtStateName")
        s.save()
        return redirect(states)
    temp={
        "state":state.objects.all()
    }
    return render(request,"state1.html",temp)

def delState(request):
    id=request.GET.get("did")
    s=state.objects.filter(stateid=id).first()
    s.delete()
    return redirect(states)

def updState(request):
    id=request.GET.get("uid")
    s=state.objects.filter(stateid=id).first()
    temp={
        "stateData":s
    }
    if request.POST.get("btnStateUpdate"):
        s.statename=request.POST.get("txtStateName")
        s.save()
        return redirect(states)
    return render(request,"updState1.html",temp)

def citys(request):
    if request.POST.get("btnCityInsert"):
        c=city()
        c.cityname=request.POST.get("txtCityName")
        c.stateid=state.objects.filter(stateid=request.POST.get("state")).first()
        c.save()
        return redirect(citys)
    temp={
        "city":city.objects.all(),
        "state":state.objects.all()
    }
    return render(request,"city1.html",temp)

def delCity(request):
    id=request.GET.get("did")
    c=city.objects.filter(cityid=id).first()
    c.delete()
    return redirect(citys)

def updCity(request):
    id=request.GET.get("uid")
    c=city.objects.filter(cityid=id).first()
    temp={
        "cityData":c,
        "state":state.objects.all()
    }
    if request.POST.get("btnCityUpdate"):
        c.cityname=request.POST.get("txtCityName")
        c.stateid=state.objects.filter(stateid=request.POST.get("state")).first()
        c.save()
        return redirect(citys)
    return render(request,"updCity1.html",temp)

def categorys(request):
    if request.POST.get("btnCatInsert"):
        c=category()
        c.categoryname=request.POST.get("txtCatName")
        c.save()
        return redirect(categorys)
    temp={
        "category":category.objects.all()
    }
    return render(request,"category1.html",temp)

def delCategory(request):
    id=request.GET.get("did")
    c=category.objects.filter(categoryid=id).first()
    c.delete()
    return redirect(states)

def updCategory(request):
    id=request.GET.get("uid")
    c=category.objects.filter(categoryid=id).first()
    temp={
        "categoryData":c
    }
    if request.POST.get("btnCatUpdate"):
        c.categoryname=request.POST.get("txtCatName")
        c.save()
        return redirect(categorys)
    return render(request,"updCategory1.html",temp)
