from django.urls import path

from . import views


app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),

    path('register/client/', views.RegisterClient.as_view(), name='client registration'),
    path('register/company/', views.RegisterCompany.as_view(), name='comapny registration'),

    path('login/client/', views.LoginClient.as_view(), name='client logining'),
    path('login/company/', views.LoginCompany.as_view(), name='comapny logining'),
]
