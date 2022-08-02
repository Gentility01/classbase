from django.urls import path
from .views import  Home, Detail, Create, Update, Delete, CustomerLogin, Register
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login', CustomerLogin.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('', Home.as_view(), name='home'),
    path('create', Create.as_view(), name = 'create'),
    path('update/<int:pk>/', Update.as_view(), name = 'update'),
    path('detail/<int:pk>/', Detail.as_view(), name='details'),
    path('delete/<int:pk>/', Delete.as_view(), name='delete'),
]