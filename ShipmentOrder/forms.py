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


class OrderCreationThreeForm(forms.ModelForm):
    # 费用
    collectFee = forms.FloatField()
    sendFee = forms.FloatField()
    transitFee = forms.FloatField()
    installFee = forms.FloatField()
    storeFee = forms.FloatField()
    packingFee = forms.FloatField()
    paymentOnAccountFreight = forms.FloatField()

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