from django.db import models

from django.utils import timezone
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)


    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=200, default='',null=True,blank=True)
    image = models.ImageField(upload_to='uploads/products/')

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
         return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()
        
    @staticmethod
    def get_product_id(ids):
        return Product.objects.filter(id__in=ids)


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)
   

    def register(self):
        self.save()

    def isExist(self):
       if Customer.objects.filter(email=self.email):
           return True
       
       return False  
    
   
 
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
        


class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=500,default='',blank=True)
    phone=models.CharField(max_length=15,default='',blank=True)
    date = models.DateField(default=timezone.now)
    status=models.BooleanField(default=False)


    def placeOrder(self):
        self.save()


    @staticmethod    
    def  get_orders_by_customers(customer_id):
         return Order.\
        objects.\
        filter(customer=customer_id).\
        order_by('-date')


