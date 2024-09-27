# order_management/web/views.py

from django.shortcuts import render
from order_management.data_handle.models import Order

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'web_handle/order_list.html', {'orders': orders})
