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
from Customers import views as customer_view
from Dispatch import views as dispatch_view
from django.contrib.auth import views as auth_views
from LogisticsERP import settings



urlpatterns = [
    # MANAGEMENT SYSTEM PAGE
    url(r'^admin/', admin.site.urls),

    # INDEX PAGE
    url(r'^index/$', main_view.index, name="load_index"),

    # ACCOUNT PAGES
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$',auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # ERROR PAGES
    url(r'^error/not-logged-in/$', main_view.error_not_logged_in, name="not_logged_in"),
    url(r'^error/redirect/$', main_view.error_redirect, name="error_redirect"),

    # ORDER PAGES
    # add order pages
    url(r'^order/add/1/$', order_view.add_order_stage_one, name="add_order_stage_one"),
    url(r'^order/add/1/customer/(?P<customer_id>[0-9]+)/$', order_view.add_order_select_customer, name="add_order_select_customer"),
    url(r'^order/add/3/$', order_view.add_order_stage_three_redirect, name="add_order_stage_three_redirect"),
    url(r'^order/add/summary/$', order_view.add_order_summary, name="add_order_summary"),
    url(r'^order/add/submit/$', order_view.add_order_audit, name="add_order_audit"),
    url(r'^order/add/goods/$', order_view.ajax_add_goods, name="add_goods"),
    url(r'^order/delete/goods/(?P<good_id>[0-9]+)/$', order_view.ajax_delete_goods, name="delete_goods"),

    # manager
    url(r'^order/track/$', order_view.track_order_manager, name="track_order_manager"),
    url(r'^order/track/detail/(?P<order_id>[0-9]+)/$', order_view.track_order_detail, name="track_order_detail"),
    url(r'^order/track/modify/(?P<order_id>[0-9]+)/$', order_view.track_order_modify, name="track_order_modify"),
    url(r'^order/track/delete/(?P<order_id>[0-9]+)/$', order_view.track_order_confirm_delete, name="track_order_confirm_delete"),
    url(r'^order/track/delete/(?P<order_id>[0-9]+)/complete/$', order_view.track_order_delete, name="track_order_delete"),
    url(r'^order/track/modify/add_good/$', order_view.ajax_add_goods_manage, name="add_goods_manage"),
    url(r'^order/track/modify/delete_good/(?P<good_id>[0-9]+)/$', order_view.ajax_delete_goods_manage, name="delete_goods_manage"),

    # draft
    url(r'^order/track/draft/$', order_view.track_order_draft, name="track_order_draft"),
    url(r'^order/track/draft/(?P<order_id>[0-9]+)/$', order_view.track_order_draft_modify, name="track_order_draft_modify"),
    url(r'^order/track/draft/(?P<order_id>[0-9]+)/submit/$', order_view.track_order_submit_audit, name="track_order_submit_audit"),

    # audit
    url(r'^order/track/audit/$', order_view.track_order_audit, name="track_order_audit"),
    url(r'^order/track/audit/(?P<order_id>[0-9]+)/$', order_view.track_order_audit_modify, name="track_order_audit_modify"),
    url(r'^order/track/audit/(?P<order_id>[0-9]+)/submit/$', order_view.track_order_audit_finalize, name="track_order_audit_finalize"),
    url(r'^pdf/(?P<order_id>[0-9]+)/$', order_view.generate_PDF, name="pdf"),

    # search
    url(r'^order/track/search/$', order_view.track_order_search, name="track_order_search"),
    url(r'^order/track/search/advanced/$', order_view.track_order_search_advanced, name="track_order_search_advanced"),
    url(r'^order/track/search/advanced/result/$', order_view.track_order_search_advanced_result, name="track_order_search_advanced_result"),
    url(r'^order/track/draft/search/$', order_view.track_order_draft_search, name="track_order_draft_search"),
    url(r'^order/track/audit/search/$', order_view.track_order_audit_search, name="track_order_audit_search"),

    # CUSTOMER MANAGEMENT PAGES
    # customer class
    url(r'^customer/class/add/$', customer_view.add_customer_class, name="add_customer_class"),
    url(r'^customer/class/$', customer_view.customer_class, name="customer_class"),
    url(r'^customer/class/detail/(?P<class_id>[0-9]+)/$', customer_view.customer_class_detail, name="customer_class_detail"),
    url(r'^customer/class/modify/(?P<class_id>[0-9]+)/$', customer_view.customer_class_modify, name="customer_class_modify"),
    url(r'^customer/class/delete/(?P<class_id>[0-9]+)/$', customer_view.customer_class_confirm_delete, name="customer_class_confirm_delete"),
    url(r'^customer/class/delete/(?P<class_id>[0-9]+)/complete/$', customer_view.customer_class_delete, name="customer_class_delete"),

    # customer
    url(r'^customer/add/$', customer_view.add_customer, name="add_customer"),
    url(r'^customer/$', customer_view.customer, name="customer"),
    url(r'^customer/detail/(?P<customer_id>[0-9]+)/$', customer_view.customer_detail, name="customer_detail"),
    url(r'^customer/modify/(?P<customer_id>[0-9]+)/$', customer_view.customer_modify, name="customer_modify"),
    url(r'^customer/delete/(?P<customer_id>[0-9]+)/$', customer_view.customer_confirm_delete, name="customer_confirm_delete"),
    url(r'^customer/delete/(?P<customer_id>[0-9]+)/complete/$', customer_view.customer_delete, name="customer_delete"),

    # search
    url(r'^customer/class/search/$', customer_view.customer_class_search, name="customer_class_search"),
    url(r'^customer/search/$', customer_view.customer_search, name="customer_search"),
    url(r'^customer/search/advanced/$', customer_view.customer_search_advanced, name="customer_search_advanced"),
    url(r'^customer/search/advanced/result/$', customer_view.customer_search_advanced_result, name="customer_search_advanced_result"),

    # DISPATCH PAGES
    # driver
    url(r'^dispatch/driver/add/$', dispatch_view.add_driver, name="add_driver"),
    url(r'^dispatch/driver/$', dispatch_view.manage_driver, name="manage_driver"),
    url(r'^dispatch/driver/detail/(?P<driver_id>[0-9]+)/$', dispatch_view.driver_detail, name="driver_detail"),
    url(r'^dispatch/driver/modify/(?P<driver_id>[0-9]+)/$', dispatch_view.driver_modify, name="driver_modify"),



]

# customized error page
handler404 = main_view.error_404
handler500 = main_view.error_500