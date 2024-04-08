from django.urls import path

from . import views


app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),

    path('register/client/', views.RegisterClient.as_view(), name='client registration'),
    path('register/company/', views.register_company, name='comapny registration'),

    path('login/client/', views.login_client, name='client logining'),
    path('login/company/', views.login_company, name='comapny logining'),
]
