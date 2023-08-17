
from django.urls import path
from .views import index 
from .views import signup,login,logout,cart,checkOut,OrderView
from .auth import auth_middleware


urlpatterns = [
   path('',index.as_view(), name='homepage'),
   path('signup',signup.as_view(),name='signup'),
   path('login',login.as_view(),name='login'),
    path('logout',logout,name='logout'),
     path('cart',cart.as_view(),name='cart'),
    path('check-out',checkOut.as_view(),name='checkout'),
    path('orders',auth_middleware(OrderView.as_view()),name='order')
]
