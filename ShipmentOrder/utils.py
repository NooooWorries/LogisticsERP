# 计算Order表的运费
# @param1: order 实例
# @param2: good 列表
def calculate_freight(order, good):
    if good.count() is 0:
        return
    freight = 0
    for item in good:
        freight = freight + item.freight
    order.freight = freight


# 计算订单货物密度
# @param1: order 实例
# @param2: good 列表
def calculate_density(order, good):
    if good.count() is 0:
        return
    total_weight = 0
    for item in good:
        total_weight = total_weight + item.weight
    order.density = (total_weight / 1000) / order.volume


# 重新排序货号
def rearrange_pack_number(good):
    for index in range(len(good)):
        good[index].pack_number = index + 1