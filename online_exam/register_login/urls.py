from django.urls import path
from . import views

urlpatterns = [

    # landing page
    # path('',views.landing_page,name='landing_page'),

    # Login section-------------------
    path('',views.landing_page,name='landing_page'),
    path('login_page',views.login_page,name='login_page'),
    path('login_submitt',views.login_submitt,name='login_submitt'),
    path('Admin_Dashboard',views.admindash,name='admindash'),

    path('register_page',views.register_page,name='register_page'),
    path('register_submit',views.register_submit,name='register_submit'),
    path('check_email',views.check_email,name='check_email'),
    path('check_phone',views.check_phone,name='check_phone'),

    # Logout section-------------------
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('student_logout',views.student_logout,name='student_logout'),


]