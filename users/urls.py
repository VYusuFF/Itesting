from django.urls import path
from .views import login_view, register, reset, main, faqs, terms

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('reset/', reset, name='reset'),
    path('main/', main, name='main'),
    path('faqs/', faqs, name='faqs'),
    path('terms/', terms, name='terms'),
]
