from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ShipmentOrder.models import ShipmentOrder
from Customers.models import Customer, CustomerClass
from Dispatch.models import DispatchRecord
from django.db.models import Q
from LogisticsERP import settings


# Create your views here.
@csrf_exempt
@login_required(login_url='/error/not-logged-in/')
def receivable_list(request):
    request.session.set_expiry(request.session.get_expiry_age())
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * settings.ONE_PAGE_OF_DATA
    endPos = startPos + settings.ONE_PAGE_OF_DATA
    order_list = ShipmentOrder.objects.filter(status=3)[startPos:endPos]
    for item in order_list:
        item.payable = item.totalPrice - item.paid_price
    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = ShipmentOrder.objects.count()
        allPage = int(allPostCounts / settings.ONE_PAGE_OF_DATA)
        remainPost = allPostCounts % settings.ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, "finance/receivable-list.html", {'order': order_list,
                                                            'allPage': allPage,
                                                            'curPage': curPage
                                                            })
