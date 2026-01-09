from django.db import models


class category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name

class product(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    quantity = models.IntegerField()
    image = models.ImageField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, blank=True, null=True)

class signup(models.Model):
    name=models.CharField(max_length=30)
    Email=models.EmailField()
    Phone=models.IntegerField()
    Password=models.CharField(max_length=10)
    pincode = models.IntegerField(null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    building_name = models.TextField(null=True)
    road_name = models.CharField(max_length=30, null=True)

class cart(models.Model):
    user_details = models.ForeignKey(signup, on_delete=models.CASCADE)
    products = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()

class wishlist(models.Model):
    user_details = models.ForeignKey(signup, on_delete=models.CASCADE)
    products = models.ForeignKey(product, on_delete=models.CASCADE)

class orders(models.Model):
    user_details = models.ForeignKey(signup, on_delete=models.CASCADE)
    product_details = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    product_status = models.CharField(max_length=30,default='order placed')
    order_date = models.DateTimeField()


class contact(models.Model):
    name = models.CharField(max_length=30)
    Email = models.EmailField()
    message=models.CharField(max_length=500)

class PasswordReset(models.Model):
    user_details = models.ForeignKey(signup,on_delete = models.CASCADE)
    token = models.CharField(max_length=255)







