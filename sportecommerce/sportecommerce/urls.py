"""
URL configuration for sportecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from sports import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('contactus', views.contactus),
    path('', views.index),
    path('categoryadd',views.categoryadd),
    path('about', views.about),
    path('login',views.userlogin),
    path('logout',views.logout),
    path('userhome',views.userhome),
    path('register',views.register),
    path('categories',views.categories),
    path('addcart/<int:d>', views.addcart),
    path('buynow/<int:p>',views.buynow),
    path('cart', views.cartview),
    path('addwishlist/<int:d>', views.addwishlist),
    path('wish_view', views.wish_view),
    path('rem/<int:d>',views.rem),
    path('remo/<int:d>',views.remo),
    path('dec/<int:d>',views.dec),
    path('inc/<int:d>',views.inc),
    path('payment/<int:id>',views.payment),
    path('adminhome',views.adminhome),
    path('addproduct',views.addproduct),
    path('manageproduct',views.manageproduct),
    path('update/<int:p>',views.update),
    path('delete/<int:v>',views.delete),
    path('view_category/<d>',views.view_category),
    path('order_sum',views.order_sum),
    path('address',views.address),
    path('success',views.order),
    path('booking_details',views.booking_details),
    path('myorder',views.myorder),
    path('booking',views.booking),
    path('update_status/<int:pk>', views.update_status),
path('forgot', views.forgot_password),
    path('reset_password/<token>', views.reset_password),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)