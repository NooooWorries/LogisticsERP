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
from django.conf.urls import url, handler404, handler500
from django.contrib import admin
from LogisticsERP import views as main_view
from ShipmentOrder import views as order_view
from Account import views as account_view
from django.contrib.auth import views as auth_views
from LogisticsERP import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # index page
    url(r'^index/$', main_view.index, name="load_index"),

    # add order pages
    url(r'^order/add/1/$', order_view.add_order_stage_one, name="add_order_stage_one"),
    url(r'^order/add/3/$', order_view.add_order_stage_three_redirect, name="add_order_stage_three_redirect"),
    url(r'^order/add/summary/$', order_view.add_order_summary, name="add_order_summary"),
    url(r'^order/add/submit/$', order_view.add_order_audit, name="add_order_audit"),
    url(r'^order/add/goods/$', order_view.ajax_add_goods, name="add_goods"),
    url(r'^order/delete/goods/(?P<good_id>[0-9]+)/$', order_view.ajax_delete_goods, name="delete_goods"),

    # track order pages
    url(r'^order/track/manage$', order_view.track_order_manager, name="track_order_manager"),

    # registration pages
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$',auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # error pages
    url(r'^error/not-logged-in/$', main_view.error_not_logged_in, name="not_logged_in"),

]

# customized error page
handler404 = main_view.error_404
handler500 = main_view.error_500