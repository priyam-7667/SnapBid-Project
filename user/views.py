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
from datetime import timedelta

# Create your views here.
def home(request):
    u=user.objects.filter(userid=request.session.get("uid")).first()
    temp={
        "img":image.objects.all().order_by('-imageid')[0:4],
        "user":user.objects.all()
    }
    return render(request,"home.html",temp)

def login(request):
    if not request.session.get("uname")==None:
        return redirect(home)
    msg={}
    if request.POST.get("btnLogin"):
        u=user.objects.filter(username=request.POST.get("txtUname"),password=request.POST.get("txtPwd")).first()
        if u==None:
            msg["error"]="Invalid Username or password"
        elif u.status==1:
            msg["error"]="The user is blocked by the admin"
        else:
            request.session["uname"]=u.username
            request.session["uid"]=u.userid
            request.session["identity"]=u.identity
            request.session["profile"]=u.profilepic.url
            request.session["cover"]=u.coverpic.url
            return redirect(home)
        
    return render(request,"login.html",msg)

def forgetPwd(request):
    u=user.objects.filter(username=request.POST.get("txtUname")).first()
    if request.POST.get("btnForgetPwd"):
        u.password=request.POST.get("txtPwd")
        u.save()
        return redirect(login)
    return render(request,"forgetPwd.html")

def logout(request):
    del request.session["uname"]
    del request.session["uid"]
    del request.session["identity"]
    del request.session["profile"]
    del request.session["cover"]
    return redirect(login)

def register(request):
    temp={
        "cities":city.objects.all()
    }
    if request.POST.get("btnReg"):
        u=user()
        u.username=request.POST.get("txtUname")
        u.password=request.POST.get("txtPwd")
        u.email=request.POST.get("txtEmail")
        u.phone=request.POST.get("txtPhone")
        u.gender=request.POST.get("gender")
        u.cityid=city.objects.filter(cityid=request.POST.get("city")).first()
        u.identity=request.POST.get("identity")
        if request.FILES.get("cup"):
            u.coverpic=request.FILES["cup"]
        if request.FILES.get("fup"):
            u.profilepic=request.FILES["fup"]
        u.save()
        return redirect(login)
    return render(request,"register.html",temp)

def myProfile(request):
    if request.session.get("uname")==None:
        return redirect(login)
    id=request.session.get("uid")
    u=user.objects.filter(userid=id).first()
    f=follow.objects.filter(userid=u,
             followersid=request.session.get("uid")
             ).first()
    followers=list(follow.objects.filter(userid=u).all())
    for x in followers:
        x.user=user.objects.filter(userid=x.followersid).first()

    following=follow.objects.filter(followersid=id).all()
    if f == None:
        doesFollows=False
    else:
        doesFollows=True
    n=notification.objects.filter(userid=u).all()
    temp={
        "u":user.objects.filter(userid=request.session.get("uid")).first(),
        "image":image.objects.filter(userid=id).all(),
        "followers":followers,
        "followings":following,
        "doesFollows":doesFollows,
        "notifications":n
    }
    return render(request,"myProfile.html",temp)

def imageInsert(request):
    if request.session.get("uname")==None:
        return redirect(login)
    temp={
        "subcat":subcategory.objects.all(),
        "u":user.objects.filter(userid=request.session.get("uid")).first()
    }
    if request.POST.get("btnImageInsert"):
        i=image()
        i.userid=user.objects.filter(userid=request.session.get("uid")).first()
        i.imagename=request.POST.get("txtName")
        if request.FILES.get("fup"):
            i.imageurl=request.FILES["fup"]
        i.freePaid=request.POST.get("freePaid")
        if request.POST.get("freePaid")=="True":
            i.mrp=request.POST.get("txtMrp")
            i.discount=request.POST.get("txtDiscount")
        i.subcategoryid=subcategory.objects.filter(subcategoryid=request.POST.get("subCategory")).first()
        i.description=request.POST.get("txtDescription")
        i.inauction=request.POST.get("inAuction")
        i.save()
        return redirect(displayImage)
    return render(request,"imageInsert.html",temp)

def updProfile(request):
    if request.session.get("uname")==None:
        return redirect(login)
    id=request.GET.get("id")
    u=user.objects.filter(userid=id).first()
    temp={
        "userData":u,
        "cities":city.objects.all()
    }
    if request.POST.get("btnUpdProfile"):
        u.username=request.POST.get("txtUname")
        u.password=request.POST.get("txtPwd")
        u.email=request.POST.get("txtEmail")
        u.phone=request.POST.get("txtPhone")
        u.gender=request.POST.get("gender")
        u.cityid=city.objects.filter(cityid=request.POST.get("city")).first()
        u.bio=request.POST.get("txtBio")
        u.identity=request.POST.get("identity")
        if request.FILES.get("cup"):
            u.coverpic=request.FILES["cup"]
        if request.FILES.get("fup"):
            u.profilepic=request.FILES["fup"]
        u.save()
        return redirect(myProfile)
    return render(request,"updProfile.html",temp)

def delImage(request):
    if request.session.get("uname")==None:
        return redirect(login)
    id=request.GET.get("did")
    i=image.objects.filter(imageid=id).first()
    i.delete()
    return redirect(myProfile)

def displayImage(request):
    img=image.objects.all()
    if request.POST.get("btnSearch"):
        img=image.objects.filter(subcategoryid=request.POST.get("subCategory")).all()
    temp={
        "image":img,
        "subcat":subcategory.objects.all()
    }
    return render(request,"displayImage.html",temp)

def followUser(request):
    uid=request.GET.get('uid')
    f=follow()
    f.userid=user.objects.filter(userid=uid).first()
    f.followersid=request.session.get("uid")
    f.save()
    if f.userid.userid != request.session["uid"]:
        notify(
            userid=f.userid.userid,
            message="%s started following you."%(request.session["uname"])
        )
    params={"uid":uid}
    url=reverse(otherProfile)
    qs=urlencode(params)
    url=f"{url}?{qs}" 
    return HttpResponseRedirect(url)

def unfollowUser(request):
    uid=request.GET.get('uid')
    f=follow.objects.filter(userid=user.objects.filter(userid=uid).first(),
             followersid=request.session.get("uid")
             ).first()
    f.delete()
    if f.userid.userid != request.session["uid"]:
        notify(
            userid=f.userid.userid,
            message="%s unfollowed you."%(request.session["uname"])
        )
    params={"uid":uid}
    url=reverse(otherProfile)
    qs=urlencode(params)
    url=f"{url}?{qs}" 
    return HttpResponseRedirect(url)

def otherProfile(request):
    id=request.GET.get("uid")
    fid=request.GET.get('fid')
    u=user.objects.filter(userid=id).first()
    f=follow.objects.filter(userid=u,
             followersid=request.session.get("uid")
             ).first()
    followers=list(follow.objects.filter(userid=u).all())
    for x in followers:
        x.user=user.objects.filter(userid=x.followersid).first()

    following=follow.objects.filter(followersid=id).all()
    if f == None:
        doesFollows=False
    else:
        doesFollows=True

    if request.POST.get("btnFollow"):
        f=follow()
        f.followersid=request.session.get("uid")
        f.userid=user.objects.filter(userid=fid).first()
        f.save()
    
    temp={
        "u":user.objects.filter(userid=id).first(),
        "image":image.objects.filter(userid=id).all(),
        "followers":followers,
        "followings":following,
        "doesFollows":doesFollows
    }
    return render(request,"otherProfile.html",temp)

def imageDetails(request):
    id=request.GET.get("id")
    u=user.objects.filter(userid=request.session.get("uid")).first()
    l=like.objects.filter(userid=u,imageid=id).first()
    img=image.objects.filter(imageid=id).first()
    img.totalviews=img.totalviews+1
    img.save()
    splitImage=str(img.imageurl)
    img.name=splitImage.split("/")[-1]
    img.price=int(float(img.mrp-img.discount))
    if l==None:
        isLiked=False
    else:
        isLiked=True

    if request.POST.get("btnCreateThread"):
        t=thread()
        t.userid=user.objects.filter(userid=request.session.get("uid")).first()
        t.imageid=image.objects.filter(imageid=id).first()
        t.title=request.POST.get("txtTitle")
        t.description=request.POST.get("txtDescription")
        t.save()
    
    od=orderes.objects.filter(userid=request.session.get('uid'),imageid=id).first()
    if od==None:
        hasbought=False
    else:
        hasbought=True
    temp={
        "i":img,
        "isLiked":isLiked,
        "hasbought":hasbought,
        "threads":thread.objects.filter(imageid=id).all(),
        "likes":like.objects.filter(imageid=id).all(),
        "user":user.objects.all()
    }
    return render(request,"imageDetails.html",temp)

def addThread(request):
    if request.session.get("uname")==None:
        return redirect(login)
    id=request.GET.get("tid")
    if request.POST.get("btnCreateComm"):
        th=threadcomment()
        th.userid=user.objects.filter(userid=request.session.get("uid")).first()
        th.comment=request.POST.get("txtctitle")
        th.threadid=thread.objects.filter(threadid=id).first()
        th.save()
    temp={
        "t":thread.objects.filter(threadid=id).first(),
        "th":threadcomment.objects.filter(threadid=id).all()
    }
    return render(request,"addThread.html",temp)

def likeImage(request):
    l=like()
    l.userid=user.objects.filter(userid=request.session["uid"]).first()
    l.imageid=image.objects.filter(imageid=request.GET.get("id")).first()
    l.save()
    if l.imageid.userid.userid != request.session["uid"]:
        notify(
            userid=l.imageid.userid.userid,
            message="%s liked your image %s"%(request.session["uname"],l.imageid.imagename)
        )
    params={"id":request.GET.get("id")}
    url=reverse(imageDetails)
    qs=urlencode(params)
    url=f"{url}?{qs}" 
    return HttpResponseRedirect(url)

def unlikeImage(request):
    userid=user.objects.filter(userid=request.session["uid"]).first()
    imageid=image.objects.filter(imageid=request.GET.get("id")).first()
    l=like.objects.filter(userid=userid,imageid=imageid).first()
    l.delete()
    if l.imageid.userid.userid != request.session["uid"]:
        notify(
            userid=l.imageid.userid.userid,
            message="%s unliked your image %s"%(request.session["uname"],l.imageid.imagename)
        )
    params={"id":request.GET.get("id")}
    url=reverse(imageDetails)
    qs=urlencode(params)
    url=f"{url}?{qs}"
    return HttpResponseRedirect(url)

def download_image(request):
    id=request.GET.get("imgid")
    img=image.objects.filter(imageid=id).first()
    img.totaldownloads=img.totaldownloads+1
    img.save()
    file_path=os.path.join(settings.MEDIA_ROOT,str(img.imageurl))
    print(file_path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path,'rb'),as_attachment=True)
    else:
        return HttpResponse("File not found.", status=404)

def wishlists(request):
    if request.session.get("uname")==None:
        return redirect(login)
    u=request.session.get('uid')
    temp={
        "likes":like.objects.filter(userid=u).all(),
        "images":image.objects.filter(userid=u).all(),
        "user":user.objects.filter(userid=request.session.get('uid')).first()
    }
    return render(request,"wishlist.html",temp)

def liveAuction(request):
    temp={
        "auction":auction.objects.all()
    }
    return render(request,"liveAuction.html",temp)

def createAuction(request):
    if request.session.get("uname")==None:
        return redirect(login)
    iid=request.GET.get("iid")
    if request.POST.get("btnCreateAuction"):
        a=auction()
        a.imageid=image.objects.filter(imageid=iid).first()
        a.userid=user.objects.filter(userid=request.session.get("uid")).first()
        a.auctionamount=request.POST.get("txtAuctionAmt")
        a.startdate=request.POST.get("startDate")
        a.enddate=request.POST.get("endDate")
        a.save()
        return redirect(myAuction)
    temp={
        "i":image.objects.filter(imageid=iid).first()
    }
    return render(request,"createAuction.html",temp)

def auctionDetails(request):
    id=request.GET.get("id")
    u=user.objects.filter(userid=request.session.get("uid")).first()
    l=like.objects.filter(userid=u,imageid=id).first()
    img=image.objects.filter(imageid=id).first()
    img.totalviews=img.totalviews+1
    img.save()
    splitImage=str(img.imageurl)
    img.name=splitImage.split("/")[-1]
    if l==None:
        isLiked=False
    else:
        isLiked=True
    b=bid.objects.filter(userid=u,imageid=id).first()
    if b==None:
        hasBidded=False
    else:
        hasBidded=True
        
    a=auction.objects.filter(imageid=img).first()
    def parse_date(date_string):
        try:
            return datetime.strptime(date_string, "%Y-%m-%d")  # Ensure correct format
        except (ValueError, TypeError):
            return None  
    a.startdate = parse_date(a.startdate)
    a.enddate = parse_date(a.enddate)

    # Check if start date is in the future
    a.not_started = a.startdate and a.startdate > datetime.now()

    if request.POST.get("btnPlaceBid"):
        b=bid()
        b.auctionid=auction.objects.filter(imageid=id).first()
        b.imageid=image.objects.filter(imageid=id).first()
        b.userid=user.objects.filter(userid=request.session.get("uid")).first()
        b.bidprice=request.POST.get("txtBidAmount")
        b.save()
    
    temp={
        "i":img,
        "isLiked":isLiked,
        "hasBidded":hasBidded,
        "likes":like.objects.filter(imageid=id).all(),
        "user":user.objects.all(),
        "bid":bid.objects.filter(auctionid=a).order_by("-bidprice").all(),
        "auction":a,
        "winBid":bid.objects.filter(auctionid=a).order_by("-bidprice").first()
    }
    return render(request,"auctionDetails.html",temp)    

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(request):
    if request.method == "POST":
        print(request.POST.get("amount"))
        orderid=request.POST.get("order_id")
        bidRec=bid.objects.filter(bidid=orderid).first()
        print("============",bidRec.bidprice)
        
        newUser=user.objects.filter(userid=bidRec.userid.userid).first()
        img=image.objects.filter(imageid=bidRec.imageid.imageid).first()
        img.userid=newUser
        img.save()
        
        a=auction.objects.filter(auctionid=bidRec.auctionid.auctionid).first()
        a.delete()
        amount = int(request.POST.get("amount")) * 100  # Convert to paisa
        
        # Create order
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",
        }
        order = razorpay_client.order.create(order_data)
        print("----",order)
        
        return JsonResponse(order)

    return JsonResponse({"error": "Invalid request"}, status=400)

def create_order2(request):
    if request.method == "POST":
        id=request.POST.get("order_id")
        uid=request.session["uid"]
        o=orderes()
        o.userid=user.objects.filter(userid=uid).first()
        o.paymentamount=int(float(request.POST.get("amount")))
        o.imageid=image.objects.filter(imageid=id).first()
        o.save()
        amount = int(request.POST.get("amount")) * 100  # Convert to paisa
        
        # Create order
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",
        }
        order = razorpay_client.order.create(order_data)
        return JsonResponse(order)

    return JsonResponse({"error": "Invalid request"}, status=400)

import hmac
import hashlib
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        client_signature = data.get("razorpay_signature")
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{data.get('razorpay_order_id')}|{data.get('razorpay_payment_id')}".encode(),
            hashlib.sha256
        ).hexdigest()

        if client_signature == generated_signature:
            return JsonResponse({"status": "Payment Successful"})

    return JsonResponse({"status": "Payment Failed"}, status=400)

def success(request):
   if request.session.get("uname")==None:
        return redirect(login)
   return render(request,"success.html")

def myAuction(request):
    if request.session.get("uname")==None:
        return redirect(login)
    temp={
        "auction":auction.objects.all()
    }
    return render(request,"myAuction.html",temp)

def notify(userid,message):
    n=notification()
    n.userid=user.objects.filter(userid=userid).first()
    n.message=message
    n.save()

def myOrder(request):
    if request.session.get("uname")==None:
        return redirect(login)
    id=user.objects.filter(userid=request.session.get("uid")).first()
    temp={
        "order":orderes.objects.filter(userid=id).all()
    }
    return render(request,"myOrder.html",temp)

def delbid(request):
    id=request.GET.get("bid")
    b=bid.objects.filter(bidid=id).first()
    b.delete()
    params={"id":request.GET.get("id")}
    url=reverse(auctionDetails)
    qs=urlencode(params)
    url=f"{url}?{qs}"
    return HttpResponseRedirect(url)

def contact(request):
    return render(request,"contact.html")

def updImage(request):
    id=request.GET.get("id")
    i=image.objects.filter(imageid=id).first()
    temp={
        "imageData":i,
        "subcat":subcategory.objects.all()
    }
    if request.POST.get("btnImageUpdate"):
        i.imagename=request.POST.get("txtName")
        if request.FILES.get("fup"):
            i.imageurl=request.FILES["fup"]
        i.freePaid=request.POST.get("freePaid")
        if request.POST.get("freePaid")=="True":
            i.mrp=request.POST.get("txtMrp")
            i.discount=request.POST.get("txtDiscount")
        i.subcategoryid=subcategory.objects.filter(subcategoryid=request.POST.get("subCategory")).first()
        i.description=request.POST.get("txtDescription")
        i.inauction=request.POST.get("inAuction")
        i.save()
        return redirect(displayImage)
    return render(request,"updImage.html",temp)