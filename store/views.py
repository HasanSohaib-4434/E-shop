from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from store.models import Product
from store.models import Category
from store.models import Customer
from store.models import Order
from store.auth import auth_middleware
from django.contrib.auth.hashers import  make_password,check_password
from django.views import View
# Create your views here.

#print(make_password('1234'))

class index(View):

    def post(self,request):
         
         product=request.POST.get('product')
         remove=request.POST.get("remove")
         cart=request.session.get('cart')
         if cart:
              quantity=cart.get(product)
              if quantity:
                   if remove:
                        if quantity<=1:
                             cart.pop(product)
                        else:
                          cart[product]=quantity-1
                   else:
                         cart[product]=quantity+1
              else:
                       cart[product]=1
         else:
              cart={}
              cart[product]=1

         request.session['cart']=cart      

         print(   request.session['cart'])
         return redirect('homepage')
         

    def get(self,request):
            cart=request.session.get('cart')
            if not cart:
                 request.session['cart']={}
            products=None
            categories=Category.get_all_categories()
            categoryId=request.GET.get('category')
            if categoryId:
                products=Product.get_all_product_by_category_id(categoryId)
            else:
                    products=Product.get_all_products()
            data={}
            data['products']=products
            data['categories']=categories
            print('you are' ,request.session.get('email'))
            # return render(request,'orders/orders.html')
            return  render (request,'index.html',data)


  


class signup(View):
    def get(self,request):
     return render(request,'signup.html')
        
    def post(self,request):
      pdata=request.POST
      first_name=pdata.get('firstname')
      last_name=pdata.get('lastname')
      phone_number=pdata.get('phonenumber')
      email=pdata.get('email')
      password=pdata.get('password')

      value={
         'first_name':first_name,
         'last_name' :last_name,
         'email':email,
         'phone_number':phone_number

      }

      errormsg=None
      customer=Customer(first_name=first_name,last_name=last_name,phone=phone_number,email=email,password=password)
      errormsg=self.validateCustomer(customer)
     
      if not errormsg:
            customer.password=make_password(customer.password)
            customer.register()

            return redirect('homepage')
      else:
            data={
                     'error':errormsg,
                     'values':value
                 }
            return render(request,'signup.html',data)

    def validateCustomer(self,customer):
        errormsg=None
        if (not customer.first_name):
            errormsg="First Name Required"
        elif  len(customer.first_name)<4:
            errormsg="First Name must be longer than 4 char"

        elif (not customer.last_name):
            errormsg="Last Name Required"
        elif  len(customer.last_name)<4:
            errormsg="Last name must be longer than 4 char"

        elif (not customer.phone):
            errormsg="Phone Number Required"
        elif  len(customer.phone)<10:
            errormsg="Phone Number must be longer than 10 char"

        elif (not customer.password):
            errormsg="Password Required"
        elif  len(customer.password)<4:
            errormsg="Password must be longer than 4 char"
        elif customer.isExist():
            errormsg="Email address Already Registerd"
        
        return  errormsg




class login(View):
     return_url=None
     def get(self,request):
            login.return_url=request.GET.get('return_url')
            return render(request,'login.html')
     def post(self,request):      
           email=request.POST.get('email')
           password=request.POST.get('password')
           customer=Customer.get_customer_by_email(email)
           errormsg=None
           if customer:
              flag = check_password(password,customer.password)
              if flag:
                   request.session['customer']=customer.id
                  
                   if login.return_url:
                      return HttpResponseRedirect(login.return_url)
                   else:
                         login.return_url=None
                         return redirect('homepage')
              else:
                    errormsg="Email or Password Invalid"
           else:
               errormsg="Email or Password Invalid"

           print(email,password)
           return render(request,'login.html', {'error':errormsg})



class cart(View):
   def get(self,request):
           ids=(list(request.session.get('cart').keys()))
           products=Product.get_product_id(ids)
           print(products)
           return render(request,'cart.html',{'products':products})

def logout(request):
     request.session.clear()
     return redirect('login')



class checkOut(View):
     def post(self,request):
          address=request.POST.get('address')
          phone=request.POST.get('phone')
          customer=request.session.get('customer')
          cart=request.session.get('cart')
          products=Product.get_product_id(list(cart.keys()))
          print(address,phone,customer,cart,products)

          for product in products:
               order=Order(customer=Customer(id=customer),product=product,price=product.price,address=address,phone=phone,quantity=cart.get(str(product.id)))
               order.save()
          request.session['cart']={}
          return redirect('cart')
           
class OrderView(View):  
     
     def get(self,request):
          customer=request.session.get('customer')
          orders=Order.get_orders_by_customers(customer)
          print(orders)
          orders=orders.reverse()
          return render(request,'orders.html',{'orders':orders})
                   