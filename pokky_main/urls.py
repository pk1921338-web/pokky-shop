from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Auth URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User Dashboard
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # Shopping
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
    # Utilities
    path('track/', views.track_order, name='track_order'),
    path('admin/print-label/<int:order_id>/', views.admin_print_label, name='admin_print_label'),
    path('webhook/shiprocket/', views.shiprocket_webhook, name='shiprocket_webhook'),
    path('my-orders/<int:order_id>/', views.user_order_detail, name='user_order_detail'),
    
    # URLs.py mein jodein
    path('secret-owner-panel-999/', views.owner_dashboard, name='owner_dashboard'),
    path('update-status/<int:order_id>/<str:new_status>/', views.update_order_status, name='update_status'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('magic-admin-creator/', views.create_superuser_jugaad),  # <--- YE LINE JODEIN
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)