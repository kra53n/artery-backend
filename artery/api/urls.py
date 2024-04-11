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

    # path('product/', None, name='get the product or products info'),
    # path('product/add/', None, name='add the product'),

    # path('order/', None, name='get the order info'),
    # path('order/take/', None, name='take the order'),

    path('cities/', views.GetAllCities.as_view(), name='get all cities'),

    path('company/cities/', views.CompanyCities.as_view(), name='get available cities for the company'),
    path('company/cities/add/', views.CompanyCitiesAdd.as_view(), name='add the city for the company'),
    path('company/cities/del/', views.CompanyCitiesDel.as_view(), name='delete the city of the company'),
    path('company/cities/edit/', views.CompanyCitiesEdit.as_view(), name='edit the city of the company'),
    path('company/roads/', views.CompanyRoads.as_view(), name='get roads of the company'),
    path('company/roads/add/', views.CompanyRoadsAdd.as_view(), name='add the roads of the company'),
    # path('company/roads/del/', views.CompanyRoadsDel.as_view(), name='delete the road of the company'),
    # path('company/roads/edit/', views.CompanyRoadsEdit.as_view(), name='edit the road of the company'),
]