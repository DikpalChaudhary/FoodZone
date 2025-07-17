from django.urls import path
from .views import admin_view,Add_item,menuITem
from .views import monthly_sales_chart,chart_view,order_list,admin_login,admin_register


urlpatterns = [
    path('', admin_view, name="admin_home"),
    path('add_item/',Add_item, name="add_item"),
    path('menuITem/',menuITem, name="menuITem"),
    path('charts/monthly-sales/', monthly_sales_chart, name='monthly_sales_chart'),
    path('charts/py_chart/', chart_view, name='py_chart'),
    path('orderlist/', order_list, name='orderlist'),
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_register/', admin_register, name='admin_register'),
    
    


]
