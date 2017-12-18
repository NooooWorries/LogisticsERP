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
from ShipmentOrder import pdf as pdf_view
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
    # manager
    url(r'^order/track/$', order_view.track_order_manager, name="track_order_manager"),
    url(r'^order/track/detail/(?P<order_id>[0-9]+)/$', order_view.track_order_detail, name="track_order_detail"),
    url(r'^order/track/modify/(?P<order_id>[0-9]+)/$', order_view.track_order_modify, name="track_order_modify"),
    url(r'^order/track/delete/(?P<order_id>[0-9]+)/$', order_view.track_order_confirm_delete, name="track_order_confirm_delete"),
    url(r'^order/track/delete/(?P<order_id>[0-9]+)/complete/$', order_view.track_order_delete, name="track_order_delete"),
    url(r'^order/track/modify/add_good/$', order_view.ajax_add_goods_manage, name="add_goods_manage"),
    url(r'^order/track/modify/delete_good/(?P<good_id>[0-9]+)/$', order_view.ajax_delete_goods_manage, name="delete_goods_manage"),

    # search
    url(r'^order/track/search/$', order_view.track_order_search, name="track_order_search"),
    url(r'^order/track/search/advanced/$', order_view.track_order_search_advanced, name="track_order_search_advanced"),
    url(r'^order/track/search/advanced/result/$', order_view.track_order_search_advanced_result, name="track_order_search_advanced_result"),
    url(r'^order/track/draft/search/$', order_view.track_order_draft_search, name="track_order_draft_search"),
    url(r'^order/track/audit/search/$', order_view.track_order_audit_search, name="track_order_audit_search"),

    # draft
    url(r'^order/track/draft/$', order_view.track_order_draft, name="track_order_draft"),
    url(r'^order/track/draft/(?P<order_id>[0-9]+)/$', order_view.track_order_draft_modify, name="track_order_draft_modify"),
    url(r'^order/track/draft/(?P<order_id>[0-9]+)/submit/$', order_view.track_order_submit_audit, name="track_order_submit_audit"),

    # audit
    url(r'^order/track/audit/$', order_view.track_order_audit, name="track_order_audit"),
    url(r'^order/track/audit/(?P<order_id>[0-9]+)/$', order_view.track_order_audit_modify, name="track_order_audit_modify"),
    url(r'^order/track/audit/(?P<order_id>[0-9]+)/submit/$', order_view.track_order_audit_finalize, name="track_order_audit_finalize"),
    url(r'^pdf/(?P<order_id>[0-9]+)/$', order_view.generate_PDF, name="pdf"),

    # registration pages
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$',auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    # error pages
    url(r'^error/not-logged-in/$', main_view.error_not_logged_in, name="not_logged_in"),
    url(r'^error/redirect/$', main_view.error_redirect, name="error_redirect"),


]

# customized error page
handler404 = main_view.error_404
handler500 = main_view.error_500