from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.account, name="account"),
    path('create/', views.create_account, name="create_account"),
    path('login/', views.login_account, name="login_account"),
    path('logout/', views.logout_account, name="logout_account"),

    path(
        'dashboard/<str:username>/',
        views.account_dashboard,
        name="account_dashboard"
    ),

    path(
        'dashboard/<str:username>/info/',
        views.account_info,
        name="account_info"
    ),

    path(
        'dashboard/<str:username>/info/change/<str:form_type>/',
        views.account_info_change,
        name="account_info_change",
    ),
]
