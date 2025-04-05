from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class state(models.Model):
    stateid=models.AutoField(primary_key=True)
    statename=models.TextField(max_length=50,null=False)

    def __str__(self):
        return self.statename

class city(models.Model):
    cityid=models.AutoField(primary_key=True)
    cityname=models.TextField(max_length=50,null=False)
    stateid=models.ForeignKey(state,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.cityname

class user(models.Model):
    userid=models.AutoField(primary_key=True)
    username=models.TextField(max_length=50)
    password=models.TextField(max_length=50)
    email=models.EmailField(max_length=254,default="megha@gmail.com")
    phone=models.IntegerField(null=False)
    gender=models.TextField(max_length=50)
    cityid=models.ForeignKey(city,on_delete=models.CASCADE,null=True)
    bio=models.TextField(max_length=200,default="Hello")
    regDate=models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=0)
    identity=models.BooleanField(default=False)
    coverpic=models.ImageField(upload_to='images/',default="images/static-1.jpg")
    profilepic=models.ImageField(upload_to='images/',default="images/default.jpg")

    def __str__(self):
        return self.username
    
class category(models.Model):
    categoryid=models.AutoField(primary_key=True)
    categoryname=models.TextField(max_length=50)

    def __str__(self):
        return self.categoryname
    
class subcategory(models.Model):
    subcategoryid=models.AutoField(primary_key=True)
    subcategoryname=models.TextField(max_length=50)
    categoryid=models.ForeignKey(category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.subcategoryname
    
class image(models.Model):
    imageid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    imagename=models.TextField(max_length=50)
    imageurl=models.ImageField(upload_to='images/',default="images/default.jpg")
    status=models.IntegerField(default=1)
    addeddate=models.DateField(auto_now=True)
    totaldownloads=models.IntegerField(default=0)
    totalviews=models.IntegerField(default=0)
    freePaid=models.BooleanField(default=False)
    mrp=models.IntegerField(default=0)
    discount=models.FloatField(default=0)
    subcategoryid=models.ForeignKey(subcategory,on_delete=models.CASCADE,null=True)
    description=models.TextField(max_length=500)
    inauction=models.BooleanField(default=False)

    def __str__(self):
        return self.imagename
    
class adminMain(models.Model):
    adminid=models.AutoField(primary_key=True)
    name=models.TextField(max_length=50)
    password=models.TextField(max_length=50)
    email=models.EmailField(max_length=254,default="admin@gmail.com")
    phone=models.IntegerField(null=False)
    profilepic=models.ImageField(upload_to='images/',default="images/default.jpg")

    def __str__(self):
        return self.name
    
class auction(models.Model):
    auctionid=models.AutoField(primary_key=True)
    imageid=models.ForeignKey(image,on_delete=models.CASCADE,null=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    createdate=models.DateTimeField(auto_now=True)
    auctionamount=models.IntegerField(null=False)
    startdate=models.TextField(null=True)
    enddate=models.TextField(null=True)
    auctionstatus=models.IntegerField(default=0)
    status=models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.auctionid)
    
class bid(models.Model):
    bidid=models.AutoField(primary_key=True)
    auctionid=models.ForeignKey(auction,on_delete=models.CASCADE,null=True)
    imageid=models.ForeignKey(image,on_delete=models.CASCADE,null=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    bidprice=models.IntegerField(null=False)
    bidtime=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bidid)
    
class bidwinner(models.Model):
    winid=models.AutoField(primary_key=True)
    imageid=models.ForeignKey(image,on_delete=models.CASCADE,null=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    auctionid=models.ForeignKey(auction,on_delete=models.CASCADE,null=True)
    bidamount=models.IntegerField(null=False)
    paymentstatus=models.IntegerField(default=0)

    def __str__(self):
        return self.widid

class follow(models.Model):
    followid=models.AutoField(primary_key=True)
    followersid=models.IntegerField(null=False)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.followid)
    
class wishlist(models.Model):
    wishlistid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    imageid=models.ForeignKey(image,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.wishlistid
    
class orderes(models.Model):
    orderid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    paymentamount=models.IntegerField(null=False)
    createdDt=models.DateField( auto_now=True, auto_now_add=False)
    imageid=models.ForeignKey(image, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.orderid)

class thread(models.Model):
    threadid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    imageid=models.ForeignKey(image,on_delete=models.CASCADE,null=True)
    status=models.IntegerField(default=0)
    createdate=models.DateTimeField(auto_now=True)
    title=models.TextField(max_length=30)
    description=models.TextField(max_length=200)

    def __str__(self):
        return self.title

class threadcomment(models.Model):
    commentid=models.AutoField(primary_key=True)
    threadid=models.ForeignKey(thread,on_delete=models.CASCADE,null=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    comment=models.TextField(max_length=50)

    def __str__(self):
        return self.comment   
    
class like(models.Model):
    likeid=models.AutoField(primary_key=True)
    imageid=models.ForeignKey(image,on_delete=models.CASCADE,null=True)
    createdate=models.DateTimeField(auto_now=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.likeid)
    
class notification(models.Model):
    notificationid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(user,on_delete=models.CASCADE,null=False)
    message=models.TextField(max_length=500)
    createdate=models.DateTimeField(auto_now=True)

class payment(models.Model):
    pass

class chat(models.Model):
    chatid=models.IntegerField(primary_key=True)
    receiverid=models.IntegerField(null=False)
    senderid=models.IntegerField(null=False)
    message=models.TextField(max_length=500,default=True)
    status=models.IntegerField(default=0)
    createddt=models.DateField(auto_now=True)
    def str(self):
         return str(self.chatid)