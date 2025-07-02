"""
URL configuration for graduation_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from tkinter.font import names

from django.contrib import admin
from django.urls import path

from new01 import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", views.index),
    path("index/", views.index),
    path("login/", views.login_view, name='login'),
    path('register/', views.register, name='register'),

    path('record_view_history/<int:house_id>/', views.record_view_history, name='record_view_history'),
    path('recommend_houses/', views.recommend_houses, name='recommend_houses'),
    path('search_houses/', views.search_houses, name='search_houses'),
    path('get_search_filters/', views.get_search_filters, name='get_search_filters'),
    path('house-distribution/', views.house_distribution, name='house-distribution'),
    path('house-type-distribution/', views.house_type_distribution, name='house-type-distribution'),
    path("data/", views.house_info_list, name='data'),

    path("administrator/", views.administrator_view, name='administrator'),  # 管理员页面
    path('delete_house/<int:house_id>/', views.delete_house, name='delete_house'),
    path('add-house/', views.add_house, name='add_house'),
]
