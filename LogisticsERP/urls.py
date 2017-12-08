"""LogisticsERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from LogisticsERP import views as index_view
from ShipmentOrder import views as order_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # inedx page
    url(r'^index/', index_view.index, name="load_index"),

    # add order page
    url(r'^order/add/1', order_view.add_order_stage_one, name="add_order_stage_one"),
    url(r'^order/add/goods', order_view.ajax_add_goods, name="add_goods"),
]
