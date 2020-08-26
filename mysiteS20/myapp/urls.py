from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'<int:top_no>', views.detail, name='top_no'),
    path(r'courses', views.courses, name='courses'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'courses/<int:cour_no>', views.coursedetail, name='cour_no'),
    path(r'login', views.user_login, name='user_login'),
    path(r'logout', views.user_logout, name='user_logout'),
    path(r'myaccount',views.myaccount, name='myaccount'),
    path(r'register',views.register, name='register'),
    path(r'forgot_password',views.forgotPassword, name = 'forgot_password')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
