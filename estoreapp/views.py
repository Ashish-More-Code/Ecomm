from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from estoreapp.models import products,Cart,Order
from django.db.models import Q
import random
# Create your views here.
def index(request):
    context={}
    p=products.objects.filter(is_active=True)
    context['products']=p
    return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=products.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    context={}
    if sv=='0':
        col='price'
    else :
        col='-price'
    p=products.objects.filter(is_active=True).order_by(col)
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=products.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        p=products.objects.filter(id=pid)
        u=User.objects.filter(id=userid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        context={}
        context['products']=p
        if len(c)==1:
            context['errmsg']="Product already exists in the cart!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product added to cart successfully"
        return render(request,'productsdetails.html',context)
    else:
        return redirect('/login')

def ulogout(request):
    logout(request)
    return redirect('/')

def productsdetails(request,pid):
    p=products.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'productsdetails.html',context)

def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    s=0
    for x in c:
        s=s+x.pid.price*x.qty
    np=len(c)
    context={}
    context['data']=c
    context['total']=s
    context['items']=np
    return render(request,'viewcart.html',context)

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect ('/viewcart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        user = authenticate(username=uname, password=upass)
        if uname=="" or upass=="" :
            context={}
            context['errmsg']="Username or Password cannot be empty"
            return render(request,'login.html',context)
        elif user is not None:
            context={}
            context['successmsg']="Login successful"
            login(request,user)
            return redirect('/')
        else:
            context={}
            context['errmsg']="Invalid username and password!"
            return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    


def uregistartion(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            context={}
            context['errmsg']="Fields cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context={}
            context['errmsg']="Password and confirm password does not match"
            return render(request,'register.html',context)
        else:
            try:
                context={}
                context['successmsg']="Registration successful"
                u=User.objects.create(username=uname,password=upass,email=uname)
                u.set_password(upass)
                u.save()
                return render(request,'register.html',context)
            except Exception:
                context={}
                context['errmsg']="User with this email id already exists !!"
                return render(request,'register.html',context)
           
    else:
        return render(request,'register.html')
    
def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        print(x.pid.name)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    np=len(orders)
    context['total']=s
    context['items']=np
    return render(request,'placeorder.html',context)

