from django.urls import path

from . import views


app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),

    path('me/', views.Me.as_view(), name='info about the user'),
    path('logout/', views.logout, name='logout the user'),

    path('register/client/', views.RegisterClient.as_view(), name='client registration'),
    path('register/company/', views.RegisterCompany.as_view(), name='comapny registration'),

    path('login/client/', views.LoginClient.as_view(), name='client logining'),
    path('login/company/', views.LoginCompany.as_view(), name='company logining'),

    # path('product/add/', None, name='add the product'),
    # path('product/get/', None, name='get the product'),

    # path('order/take/', None, name='take an order'),
    # path('order/info/', None, name='recieve an information about order'),

    path('company/cities/', views.CompanyCities.as_view(), name='recieve an cities available for the company'),
]