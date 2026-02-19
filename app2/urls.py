from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_user, name='register_user'),
    path('users/', views.view_users, name='view_users'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('create-department/', views.create_department, name='create_department'),
    path('create-master/', views.create_master, name='create_master'),
    
    path('departments/', views.view_departments, name='view_departments'),
    path('departments/update/<int:dept_id>/', views.update_department, name='update_department'),
    path('departments/delete/<int:dept_id>/', views.delete_department, name='delete_department'),

    # Master
    path('masters/', views.view_masters, name='view_masters'),
    path('masters/update/<int:master_id>/', views.update_master, name='update_master'),
    path('masters/delete/<int:master_id>/', views.delete_master, name='delete_master'),
    path('my-info/', views.view_personal_info, name='view_personal_info'),
    path('my-profile/', views.view_my_profile, name='view_my_profile'),
    path('view-attendance/', views.view_attendance, name='view_attendance'),

]
