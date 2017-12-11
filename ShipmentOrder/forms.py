from django import forms
from django.contrib.auth.models import User
from django.db import models
from ShipmentOrder.models import UserProfile, CustomerClass, Customer, ShipmentOrder, Goods


class OrderCreationOneForm(forms.ModelForm):
    # 发货人信息
    sender = forms.CharField(required=True,
                             label="发件人",
                             widget=forms.TextInput(attrs={'placeholder': '输入发件人姓名'}),
                             error_messages={'required': '此为必填项目'}
                             )
    from_address = forms.CharField(required=True,
                                   label="发件地址",
                                   widget=forms.TextInput(attrs={'placeholder': '输入发件人地址'}),
                                   error_messages={'required': '此为必填项目'})
    sender_contact = forms.CharField(required=True,
                                     label="发件人联系方式",
                                     widget=forms.TextInput(attrs={'placeholder': '输入发件人联系电话'}),
                                     error_messages={'required': '此为必填项目'})

    # 收货人信息
    receiver = forms.CharField(required=True,
                               label="收件人",
                               widget=forms.TextInput(attrs={'placeholder': '输入收件人姓名'}),
                               error_messages={'required': '此为必填项目'})
    to_address = forms.CharField(required=True,
                                 label="收件地址",
                                 widget=forms.TextInput(attrs={'placeholder': '输入收件人地址'}),
                                 error_messages={'required': '此为必填项目'})
    receiver_contact = forms.CharField(required=True,
                                       label="收件人联系方式",
                                       widget=forms.TextInput(attrs={'placeholder': '输入收件人联系电话'}),
                                       error_messages={'required': '此为必填项目'})

    # 其他
    mode = forms.CharField(required=True,
                           label="运送模式",
                           widget=forms.TextInput(attrs={'placeholder': '输入运送模式'}),
                           error_messages={'required': '此为必填项目'}
                           )
    comments = forms.CharField(required=False,
                               label="备注",
                               widget=forms.Textarea(attrs={'placeholder': '输入订单备注'})
                               )

    class Meta:
        model = ShipmentOrder
        fields = ("sender", "from_address", "sender_contact", "receiver", "to_address",
                  "receiver_contact", "mode", "comments",)

    def save(self, commit=True):
        order_form = super(OrderCreationOneForm, self).save(commit=False)
        order_form.sender = self.cleaned_data["sender"]
        order_form.from_address = self.cleaned_data["from_address"]
        order_form.sender_contact = self.cleaned_data["sender_contact"]
        order_form.receiver = self.cleaned_data["receiver"]
        order_form.to_address = self.cleaned_data["to_address"]
        order_form.receiver_contact = self.cleaned_data["receiver_contact"]
        order_form.mode = self.cleaned_data["mode"]
        order_form.comments = self.cleaned_data["comments"]
        if commit:
            order_form.save()
        return order_form


class OrderCreationTwoForm(forms.ModelForm):
    goods_name = forms.CharField(required=True,
                                 label="货物名称",
                                 widget=forms.TextInput(attrs={'placeholder': '输入货物名称'}),
                                 error_messages={'required': '此为必填项目'})
    amount = forms.FloatField(required=True,
                              label="数量",
                              widget=forms.NumberInput(attrs={'placeholder': '输入货物数量'}),
                              error_messages={'required': '此为必填项目'})
    volume = forms.FloatField(required=True,
                              label="体积",
                              widget=forms.NumberInput(attrs={'placeholder': '输入货物体积'}),
                              error_messages={'required': '此为必填项目'})
    weight = forms.FloatField(required=True,
                              label="重量",
                              widget=forms.NumberInput(attrs={'placeholder': '输入货物重量'}),
                              error_messages={'required': '此为必填项目'})
    freight = forms.FloatField(required=True,
                              label="运费",
                              widget=forms.NumberInput(attrs={'placeholder': '输入运费（总和）'}),
                              error_messages={'required': '此为必填项目'})
    claim_value = forms.FloatField(required=True,
                                   label="声明价值",
                                   widget=forms.NumberInput(attrs={'placeholder': '输入货物声明价值（总和）'}),
                                   error_messages={'required': '此为必填项目'})
    insurance_rate = forms.FloatField(required=True,
                                      label="保价费率",
                                      widget=forms.NumberInput(attrs={'placeholder': '输入保价费用费率'}),
                                      error_messages={'required': '此为必填项目'})

    class Meta:
        model = Goods
        fields = ("goods_name", "amount", "volume", "weight", "freight", "claim_value", "insurance_rate")

    def save(self, commit=True):
        goods_form = super(OrderCreationTwoForm, self).save(commit=False)
        goods_form.goods_name = self.cleaned_data["goods_name"]
        goods_form.amount = self.cleaned_data["amount"]
        goods_form.volume = self.cleaned_data["volume"]
        goods_form.weight = self.cleaned_data["weight"]
        goods_form.freight = self.cleaned_data["freight"]
        goods_form.claim_value = self.cleaned_data["claim_value"]
        goods_form.insurance_rate = self.claim_value["insurance_rate"]
        if commit:
            goods_form.save()
        return goods_form


class OrderCreationThreeForm(forms.ModelForm):
    # 费用
    collectFee = forms.FloatField(required=True,
                                  label="接货费",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入接货费用'}),
                                  error_messages={'required': '此为必填项目'})
    sendFee = forms.FloatField(required=True,
                               label="送货费",
                               widget=forms.NumberInput(attrs={'placeholder': '输入送货费用'}),
                               error_messages={'required': '此为必填项目'})
    transitFee = forms.FloatField(required=True,
                                  label="中转费",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入中转费用'}),
                                  error_messages={'required': '此为必填项目'})
    installFee = forms.FloatField(required=True,
                                  label="装卸费",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入装卸费用'}),
                                  error_messages={'required': '此为必填项目'})
    storeFee = forms.FloatField(required=True,
                                label="保管费",
                                widget=forms.NumberInput(attrs={'placeholder': '输入保管费用'}),
                                error_messages={'required': '此为必填项目'})
    packingFee = forms.FloatField(required=True,
                                  label="包装费",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入包装费用'}),
                                  error_messages={'required': '此为必填项目'})
    paymentOnAccountFreight = forms.FloatField(required=True,
                                               label="垫货运费",
                                               widget=forms.NumberInput(attrs={'placeholder': '输入已垫付费用'}),
                                               error_messages={'required': '此为必填项目'})

    class Meta:
        model = ShipmentOrder
        fields = ("collectFee", "sendFee",
                  "transitFee", "installFee", "storeFee", "packingFee", "paymentOnAccountFreight")

    def save(self, commit=True):
        order_form = super(OrderCreationThreeForm, self).save(commit=False)
        order_form.collectFee = self.cleaned_data["collectFee"]
        order_form.sendFee = self.cleaned_data["sendFee"]
        order_form.transitFee = self.cleaned_data["transitFee"]
        order_form.installFee = self.cleaned_data["installFee"]
        order_form.storeFee = self.cleaned_data["storeFee"]
        order_form.packingFee = self.cleaned_data["packingFee"]
        order_form.paymentOnAccountFreight = self.cleaned_data["paymentOnAccountFreight"]