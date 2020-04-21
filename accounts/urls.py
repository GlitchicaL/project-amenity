from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.account, name="account"),
    path('create/', views.create_account, name="create_account"),
    path('login/', views.login_account, name="login_account"),
    path('logout/', views.logout_account, name="logout_account"),

    # NOTE: Paths listed below here require the user to be logged in
    path(
        '<str:username>/dashboard/',
        views.account_dashboard,
        name="account_dashboard"
    ),

    # The following paths deal with the user's cart, and placing an order
    path('<str:username>/cart/', views.account_cart, name="account_cart"),
    path(
        '<str:username>/cart/empty-cart/',
        views.account_empty_cart,
        name="account_empty_cart"
    ),
    path(
        '<str:username>/cart/place-order/',
        views.account_place_order,
        name="account_place_order"
    ),

    # These paths allow the user to view all or a specific order
    path('<str:username>/orders/', views.account_orders, name="account_orders"),
    path(
        '<str:username>/order/<int:order_id>/',
        views.account_view_order,
        name="account_view_order"
    ),
    path(
        '<str:username>/order/<int:order_id>/cancel-order/',
        views.account_cancel_order,
        name="account_cancel_order"
    ),

    # These paths allow the user to view/change his/her information (ex. Address, email, etc.)
    path(
        '<str:username>/info/',
        views.account_info,
        name="account_info"
    ),

    path(
        '<str:username>/info/change-info/<str:form_type>/',
        views.account_info_change,
        name="account_info_change",
    ),
]
