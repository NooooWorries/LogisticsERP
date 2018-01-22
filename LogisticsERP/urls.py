# LogisticsERP URL Configuration
from django.conf.urls import url, handler404, handler500
from django.contrib import admin
from LogisticsERP import views as main_view
from ShipmentOrder import views as order_view
from Customers import views as customer_view
from Dispatch import views as dispatch_view
from Export import views as export_view
from Diagram import views as diagram_view
from Finance import views as finance_view
from Account import views as account_view
from django.contrib.auth import views as auth_views
from LogisticsERP import settings
from Account.forms import LoginForm


urlpatterns = [
    # MANAGEMENT SYSTEM PAGE
    url(r'^admin/', admin.site.urls),

    # INDEX PAGE
    url(r'^index/$', main_view.index, name="load_index"),

    # ACCOUNT PAGES
    url(r'^login/$', auth_views.login, name='login', kwargs={"authentication_form": LoginForm}),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

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
    url(r'^order/track/modify/2/(?P<order_id>[0-9]+)/$', order_view.track_order_modify_2, name="track_order_modify_2"),
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
    url(r'^order/track/audit/2/(?P<order_id>[0-9]+)/$', order_view.track_order_audit_modify_2, name="track_order_audit_modify_2"),
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
    url(r'^dispatch/driver/search/$', dispatch_view.driver_search, name="driver_search"),
    url(r'^dispatch/driver/detail/(?P<driver_id>[0-9]+)/$', dispatch_view.driver_detail, name="driver_detail"),
    url(r'^dispatch/driver/modify/(?P<driver_id>[0-9]+)/$', dispatch_view.driver_modify, name="driver_modify"),
    url(r'^dispatch/driver/delete/(?P<driver_id>[0-9]+)/$', dispatch_view.driver_delete, name="driver_delete"),

    # add dispatch record
    url(r'^dispatch/order/add/1/$', dispatch_view.add_dispatch_order, name="add_dispatch_order"),
    url(r'^dispatch/order/add/2/(?P<order_id>[0-9]+)/$', dispatch_view.add_dispatch_order_choose_good, name="add_dispatch_order_choose_good"),
    url(r'^dispatch/order/choose/(?P<order_id>[0-9]+)/(?P<good_id>[0-9]+)/$', dispatch_view.ajax_select_good, name="ajax_select_good"),
    url(r'^dispatch/order/choose/(?P<good_id>[0-9]+)/cancel/$', dispatch_view.ajax_select_good_cancel, name="ajax_select_good_cancel"),
    url(r'^dispatch/order/add/3/(?P<order_id>[0-9]+)/$', dispatch_view.add_dispatch_order_summary, name="add_dispatch_order_summary"),
    url(r'^dispatch/order/pdf/(?P<order_id>[0-9]+)/$', dispatch_view.generate_PDF, name="generate_dispatch_pdf"),

    # manage dispatch record
    url(r'^dispatch/order/$', dispatch_view.manage_dispatch_order, name="manage_dispatch_order"),

    url(r'^dispatch/order/detail/(?P<order_id>[0-9]+)/$', dispatch_view.dispatch_order_detail, name="dispatch_order_detail"),
    url(r'^dispatch/order/modify/(?P<order_id>[0-9]+)/$', dispatch_view.dispatch_order_modify, name="dispatch_order_modify"),
    url(r'^dispatch/order/delete/(?P<order_id>[0-9]+)/$', dispatch_view.dispatch_order_delete, name="dispatch_order_delete"),

    # dispatch record draft
    url(r'^dispatch/order/draft/$', dispatch_view.draft_dispatch_order, name="draft_dispatch_order"),

    # arrival
    url(r'^dispatch/order/arrival/$', dispatch_view.arrival_dispatch_order, name="arrival_dispatch_order"),
    url(r'^dispatch/order/arrival/(?P<order_id>[0-9]+)/$', dispatch_view.arrival_dispatch_order_detail, name="arrival_dispatch_order_detail"),
    url(r'^dispatch/order/arrival/(?P<order_id>[0-9]+)/confirm/$', dispatch_view.arrival_dispatch_order_confirm, name="arrival_dispatch_order_confirm"),

    # search
    url(r'^dispatch/order/search/$', dispatch_view.dispatch_order_search, name="dispatch_order_search"),
    url(r'^dispatch/order/search/advanced/$', dispatch_view.dispatch_order_search_advanced, name="dispatch_order_search_advanced"),
    url(r'^dispatch/order/search/advanced/result/$', dispatch_view.dispatch_order_search_advanced_result, name="dispatch_order_search_advanced_result"),


    # EXPORT DATA SHEET PAGES
    # export shipment order
    url(r'^export/order/$', export_view.export_order, name="export_order"),
    url(r'^export/order/result/$', export_view.export_order_result, name="export_order_result"),

    # export customer
    url(r'^export/customer/$', export_view.export_customer, name="export_customer"),
    url(r'^export/customer/result/$', export_view.export_customer_result, name="export_customer_result"),


    # export dispatch order
    url(r'^export/dispatch/$', export_view.export_dispatch_order, name="export_dispatch_order"),
    url(r'^export/dispatch/result/$', export_view.export_dispatch_order_result, name="export_dispatch_order_result"),

    # export payment order
    url(r'^export/finance/$', export_view.export_payment_order, name="export_payment_order"),
    url(r'^export/finance/result/$', export_view.export_payment_order_result, name="export_payment_order_result"),


    # DIAGRAM PAGES
    # shipment order
    url(r'^diagram/order/$', diagram_view.order_diagram, name="order_diagram"),
    url(r'^diagram/order/weekly/$', diagram_view.ajax_order_weekly, name="ajax_order_weekly"),
    url(r'^diagram/order/monthly/$', diagram_view.ajax_order_monthly, name="ajax_order_monthly"),
    url(r'^diagram/order/yearly/$', diagram_view.ajax_order_yearly, name="ajax_order_yearly"),
    url(r'^diagram/order/customize/$', diagram_view.ajax_order_customize, name="ajax_order_customize"),

    # dispatch record
    url(r'^diagram/dispatch/$', diagram_view.dispatch_order_diagram, name="dispatch_order_diagram"),
    url(r'^diagram/dispatch/weekly/$', diagram_view.ajax_dispatch_order_weekly, name="ajax_dispatch_order_weekly"),
    url(r'^diagram/dispatch/monthly/$', diagram_view.ajax_dispatch_order_monthly, name="ajax_dispatch_order_monthly"),
    url(r'^diagram/dispatch/yearly/$', diagram_view.ajax_dispatch_order_yearly, name="ajax_dispatch_order_yearly"),
    url(r'^diagram/dispatch/customize/$', diagram_view.ajax_dispatch_order_customize, name="ajax_dispatch_order_customize"),

    # payment record
    url(r'^diagram/finance/$', diagram_view.payment_order_diagram, name="payment_order_diagram"),
    url(r'^diagram/finance/weekly/$', diagram_view.ajax_payment_order_weekly, name="ajax_payment_order_weekly"),
    url(r'^diagram/finance/monthly/$', diagram_view.ajax_payment_order_monthly, name="ajax_payment_order_monthly"),
    url(r'^diagram/finance/yearly/$', diagram_view.ajax_payment_order_yearly, name="ajax_payment_order_yearly"),
    url(r'^diagram/finance/customize/$', diagram_view.ajax_payment_order_customize, name="ajax_payment_order_customize"),


    # FINANCE PAGES
    # add payment record
    url(r'^finance/receivable/$', finance_view.receivable_list, name="receivable_list"),
    url(r'^finance/receivable/pay/(?P<order_id>[0-9]+)/$', finance_view.make_payment, name="make_payment"),

    # manage
    url(r'^finance/manage/$', finance_view.manage_payment_record, name="manage_payment_record"),
    url(r'^finance/manage/(?P<order_id>[0-9]+)/detail$', finance_view.payment_record_detail, name="payment_record_detail"),
    url(r'^finance/manage/(?P<order_id>[0-9]+)/modify$', finance_view.payment_record_modify,
        name="payment_record_modify"),

    # search
    url(r'^finance/search/$', finance_view.payment_order_search, name="payment_order_search"),
    url(r'^finance/search/advanced/$', finance_view.payment_order_search_advanced, name="payment_order_search_advanced"),
    url(r'^finance/search/advanced/result/$', finance_view.payment_order_search_advanced_result, name="payment_order_search_advanced_result"),


    # SYSTEM MANAGEMENT PAGES
    # add account
    url(r'^system/user/$', account_view.add_account, name="add_account"),

]

# customized error page
handler404 = main_view.error_404
handler500 = main_view.error_500

# change title of admin site
admin.site.site_header = '物流管理系统 - 超级管理员后台'
admin.site.site_title = '物流管理系统'
