from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
import razorpay
def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Email = request.POST.get('Email')
        message = request.POST.get('message')
        print(name,Email,message)
        contact_us = contact.objects.create(name=name, Email=Email, message=message)
        contact_us.save()
        messages.success(request, "Message sent successfully!")
        return redirect(contactus)
    return render(request, 'contact.html')
def categoryadd(request):
    if request.method == 'POST':
        name = request.POST.get('category_name')
        if category.objects.filter(name=name).exists():
            messages.error(request, "This category already exists.")
        else:
            category.objects.create(name=name)
            messages.success(request, "Category added successfully!")
            return redirect(categoryadd)
    return render(request, 'categoryadd.html')

def about(request):
    return render(request,'about.html')

def index(request):
    categories = product.objects.all()
    return render(request, 'index.html', {'data': categories})
def shoes(request):
    return render(request,'shoes.html')

def categories(request):
    data = product.objects.all()
    return render(request, 'categories.html', {'data': data})

def userlogin(request):
    if request.method == 'POST':
        a = request.POST['mail']
        d = request.POST['pass']
        try:
            data = signup.objects.get(Email=a)
            print(data,data.Password)
            if data.Password == d:
                    request.session['user'] = a
                    messages.success(request, 'login successful')
                    return redirect(userhome)
            else:
                    messages.error(request, 'incorrect pass!')
                    return redirect(userlogin)
        except Exception as e:
            print(e)
            if a == 'admin@gmail.com' and d == '12345':
                request.session['alwin'] = a
                return redirect(adminhome)
            else:
                messages.error(request, 'incorrect')
                return redirect(userlogin)
    return render(request, "login.html")

def logout(request):
    if 'user' in request.session or 'admin' in request.session:
        request.session.flush()
        return redirect(userlogin)
    return redirect(userlogin)




def userhome(request):
    data = category.objects.all()
    d = product.objects.all()
    return render(request, 'userhome.html', {'data': data, 'd': d})


def register(request):
    if request.method=='POST':
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n6']
        e=request.POST['n7']
        if signup.objects.filter(Email=b).exists():
            messages.success(request,"Email already exists")
            return redirect(register)
        elif signup.objects.filter(Phone=c).exists():
            messages.success(request,"Phone number already exists")
            return redirect(register)
        else:
            if d==e:
                signup.objects.create(name=a, Email=b, Phone=c, Password=d).save()
                return render(request, 'register.html')
            else:
                messages.error(request,'password doesnot match')
                return redirect(register)
    return render(request,'register.html')


def adminhome(request):
    return render(request, 'adminhome.html')


def addproduct(request):
    cate=category.objects.all()
    if request.method == 'POST':
        a = request.POST['name']
        b = request.POST['price']
        c = request.POST['quantity']
        cat = request.POST['category']
        print("===============")
        print(cat)
        p = request.FILES['image']
        size = request.POST.get('size', '')
        print(size)

        selected_category = category.objects.get(name=cat)
        if selected_category.name in ['jerseys', 'footballboots'] and not size:
            messages.error(request,'Size is required for this category.')
            return redirect(addproduct)
        else:
            product.objects.create(
                name=a,
                price=b,
                quantity=c,
                image=p,
                category=selected_category,
                size=size if selected_category.name in ['Jersey', 'Football boots'] else None
            )
            return render(request, 'addproduct.html')

    return render(request, 'addproduct.html',{'cate':cate})


# def addproduct(request):
#     if request.method == 'POST':
#         a = request.POST['name']
#         b = request.POST['price']
#         c = request.POST['quantity']
#         p = request.FILES['image']
#         product.objects.create(name=a, price=b, quantity=c,image=p).save()
#         return render(request,'addproduct.html',{'a':a,'b':b,'c':c,'p':p})
#     return render(request,'addproduct.html')

def booking_details(request):
    data = orders.objects.all()
    return render(request,'booking_details.html',{'data':data})
def manageproduct(request):
    data = product.objects.all()
    return render(request,'manageproduct.html',{'data':data})

def update(request,p):
        data = product.objects.get(pk=p)
        form=modelform(instance=data)
        if request.method=='POST':
            form=modelform(request.POST,request.FILES,instance=data)
            if form.is_valid():
                form.save()
                return redirect(manageproduct)
        return render(request, 'update.html', {'data': form})


def delete(request,v):
    data=product.objects.get(pk=v)
    data.delete()
    return redirect(manageproduct)

def addcart(request, d):
    if 'user' not in request.session:
        return redirect('userlogin')
    user = signup.objects.get(Email=request.session['user'])
    item = product.objects.get(pk=d)

    cart_item, created = cart.objects.get_or_create(
        user_details=user,
        products=item,
        total_price= item.price
    )
    if not created:
        cart_item.quantity += 1
        cart_item.totalprice = cart_item.quantity * item.price
        cart_item.save()
        print("saved")
    return redirect(cartview)
def buynow(request,p):
    if 'user' not in request.session:
        return redirect('userlogin')
    user = signup.objects.get(Email=request.session['user'])
    item = product.objects.get(pk=p)

    cart_item, created = cart.objects.get_or_create(
        user_details=user,
        products=item,
        total_price= item.price
    )
    if not created:
        cart_item.quantity += 1
        cart_item.totalprice = cart_item.quantity * item.price
        cart_item.save()
        print("saved")
    return redirect(view_category,item.category.name)


def cartview(request):
    if 'user' in request.session:
        user = signup.objects.get(Email=request.session['user'])
        data = cart.objects.filter(user_details=user)
        total = sum(item.total_price for item in data)
        qty = sum(item.quantity for item in data)
        return render(request, 'cart.html', {"data": data, "total": total, "qty": qty})
    else:
        return redirect(userlogin)

def addwishlist(request,d):
    pro = product.objects.get(pk=d)
    if wishlist.objects.filter(products=pro).exists():
        messages.error(request,'Item Already Added To Wishlist')
        return redirect(view_category)
    else:
        user=signup.objects.get(Email=request.session['user'])
        wishlist.objects.create(user_details=user,products=pro).save()
        messages.success(request,'Item Added To Your Wishlist')
        return redirect(wish_view)
def wish_view(request):
    user = signup.objects.get(Email=request.session['user'])
    data = wishlist.objects.filter(user_details=user)
    return render(request,'wishlist.html',{'data':data})

def remo(request,d):
    data=wishlist.objects.get(pk=d)
    data.delete()
    return redirect(wish_view)

def rem(request,d):
    data=cart.objects.get(pk=d)
    data.delete()
    return redirect(cartview)


def view_category(request,d):
    data = category.objects.all()
    d= category.objects.get(name=d)
    print(d)
    data1=product.objects.filter(category=d)
    print(data1)
    return render(request, 'view_category.html',{'data':data,'data1':data1})


def inc(request,d):
    print("hellloooo")
    if 'user' in request.session:
        data=cart.objects.get(pk=d)
        print("cart_inc",data)
        if data.quantity < data.products.quantity:
            data.quantity+=1
            data.total_price=data.quantity*data.products.price
            data.save()
            return redirect(cartview)
        else:
            messages.error(request,'Out oF stock')
            return redirect(cartview)
    return redirect(userlogin)
def dec(request,d):
    data=cart.objects.get(pk=d)
    if data.quantity>1 :
        data.quantity -= 1
        data.total_price=data.quantity*data.products.price
        data.save()
        return redirect(cartview)
    else:
        data.delete()
        return redirect(cartview)
def remove(request,d):
    data=cart.objects.get(pk=d)
    data.delete()
    return redirect(cartview)

def order(request):
    user = signup.objects.get(Email=request.session['user'])
    data = cart.objects.filter(user_details=user)
    import datetime
    d = datetime.datetime.now()
    for i in data:
        a=product.objects.get(name=i.products.name)
        a.quantity=a.quantity-i.quantity
        print(a.quantity)
        a.save()
        orders.objects.create(user_details=user,product_details=a,quantity=i.quantity,amount=i.total_price,order_date=d).save()
    data.delete()
    return render(request,"success.html")
def payment(request, id):
    amount = id * 100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "payment.html", {'amount': amount})


def address(request):
    user = signup.objects.get(Email=request.session['user'])
    if request.method == 'POST':
        x=request.POST['x1']
        y=request.POST['x2']
        z=request.POST['x3']
        a = request.POST['x4']
        b = request.POST['x5']
        c = request.POST['x6']
        d = request.POST['x7']
        e = request.POST['x8']
        user.name=x
        user.email=y
        user.phone=z
        user.pincode=a
        user.state=b
        user.city=c
        user.building_name=d
        user.road_name=e
        user.save()
        messages.success(request,'Address Added successfully')
        return redirect(order_sum)
    return render(request,'address.html',{'user':user})

def order_sum(request):
    user=signup.objects.get(Email=request.session['user'])
    data=cart.objects.filter(user_details=user)
    total = 0
    quantity = 0
    for i in data:
        total += i.total_price
        quantity += 1
    return render(request, 'order_summary.html', {'data': data, 'total': total, 'quantity': quantity,'user':user })

def myorder(request):
    user = signup.objects.get(Email=request.session['user'])
    data = orders.objects.filter(user_details=user)
    return render(request,'myorder.html',{'data':data})


def update_status(request, pk):
    if request.method == 'POST':
        if orders.objects.filter(pk=pk).exists():
            order = orders.objects.get(pk=pk)
            new_status = request.POST.get('n1')
            if new_status:
                order.product_status = new_status
                order.save()
                return redirect(booking)
    return redirect(booking)

def booking(request):
    data = orders.objects.all()
    return render(request,'booking_details.html',{'data':data})

from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = signup.objects.get(Email=email)
        except Exception as e:
            print (e)# noqa: E722
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user_details=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset_password/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:  # noqa: E722
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forgot.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user_details.Password=new_password
            password_reset.user_details.save()
            # password_reset.delete()
            return redirect(userlogin)
    return render(request, 'reset_password.html', {'token': token})