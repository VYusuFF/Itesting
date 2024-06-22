from django.urls import path
from .views import dashboard, profile, test_add, test_edit, test_delete, test_solve, test_result, logout_view

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('test_add/', test_add, name='test_add'),
    path('test_edit/<int:test_id>/', test_edit, name='test_edit'),
    path('test_delete/<int:test_id>/', test_delete, name='test_delete'),
    path('test/<int:test_id>/solve/', test_solve, name='test_solve'),
    path('test/<int:test_id>/result/', test_result, name='test_result'),
    path('logout/', logout_view, name='logout'),
]