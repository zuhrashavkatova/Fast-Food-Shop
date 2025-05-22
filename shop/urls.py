from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Custom admin panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/add/', views.add_product, name='add_product'),
    path('admin-panel/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin-panel/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
