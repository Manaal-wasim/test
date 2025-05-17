from django.urls import path
from . import shop_views
from .shop_views import api
# from .views import luxury_gallery,home,cart_view,logout_view,checkout_view
from . import views
from accounts import views as accounts_views


urlpatterns = [
    path('', views.home, name='home'),  # Home page (already defined)
    path('luxury-gallery/', views.luxury_gallery, name='luxury-gallery'),
    path('api/cart/', api.ajax_cart_update, name='ajax-cart'),
    path('cart/', views.view_cart, name='cart'),  # Cart page
    path('history/', views.order_history, name='order_history'),
    # path('login/', views.login_view, name='login'),
    path('login/', accounts_views.login_view, name='login'),
    # path('register/', views.register_view, name='register'),
    path('register/', accounts_views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('feedback/<int:order_id>/', views.give_feedback, name='give_feedback')
    ]
