from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.login ,name='login'),
    path('signup',views.signup ,name='signup'),
    path('home',views.home ,name='home' ), 
    path('add_to_cart',views.add_to_cart ,name='add_to_cart'),
    path('add_to_cart/<int:item_no>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout_cart/', views.checkout_cart, name='checkout_cart'),
    path('checkout',views.checkout,name='checkout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_title="The FoodStore"
admin.site.site_header="The FoodStore Admin"


# username=dikpalchy
# password =123456