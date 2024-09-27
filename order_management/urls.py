"""
URL configuration for order_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from . import views

urlpatterns = [
    path('admin/', admin.site.urls), # '/admin/' URL로 접속하면 Django의 어드민 페이지로 연결
    #path('', views.order_list, name='order_list'), # 루트 URL ('/')로 접속하면 'order_list' 뷰가 호출
    path('', include('order_management.web.urls')),  # web 폴더의 urls.py 포함
]

