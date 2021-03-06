from django.urls import include, path

from . import views

urlpatterns = [
    #------------------------------------------------------------------------------------------------------------------------------#
    ### USER REGISTRATION PATHS ###

    path('account/', views.account, name="login_page"),
    path('create-account/', views.create_account, name="create_account"),

    #------------------------------------------------------------------------------------------------------------------------------#
    ### USER LOGIN PATHS ###

    path('login-account/', views.login_account, name="login_account"),
    path('logout/', views.logout_account, name="logout_account"),

    #------------------------------------------------------------------------------------------------------------------------------#
    # NOTE: Paths listed below here require the user to be logged in

    path('dashboard/', views.account_dashboard, name="account_dashboard"),

    path('dashboard/remove-cart-item/',
         views.account_remove_from_cart),

    path('dashboard/edit-cart-quantity/',
         views.account_edit_cart_quantity),

    #------------------------------------------------------------------------------------------------------------------------------#
    ### USER CART PATHS ###

    path('cart/', views.account_cart, name="account_cart"),
    path('cart/empty-cart/', views.account_empty_cart, name="account_empty_cart"),
    path('cart/place-order/', views.account_place_order,
         name="account_place_order"),

    path('cart/remove-cart-item/', views.account_remove_from_cart,
         name="account_remove_from_cart"),

    path('cart/edit-cart-quantity/', views.account_edit_cart_quantity),

    #------------------------------------------------------------------------------------------------------------------------------#
    ### USER ORDER PATHS ###

    path('orders/', views.account_orders, name="account_orders"),
    path('order/<int:order_id>/', views.account_view_order,
         name="account_view_order"),

    path('order/<int:order_id>/cancel-order/',
         views.account_cancel_order, name="account_cancel_order"),

    #------------------------------------------------------------------------------------------------------------------------------#
    ### USER INFO/SETTINGS PATHS ###

    path('info/', views.account_info, name="account_info"),
    path('info/change-info/<str:form_type>/',
         views.account_info_change, name="account_info_change"),
]
