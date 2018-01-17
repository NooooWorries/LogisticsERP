from django import forms
from Finance.models import PaymentOrder
import datetime
from django.core.exceptions import ValidationError


class PaymentOrderCreationForm(forms.ModelForm):
    amount = forms.FloatField(required=True,
                              label="付款金额",
                              widget=forms.NumberInput(attrs={'placeholder': '输入付款金额'}),
                              error_messages={'required': '此为必填项目'}
                              )
    comments = forms.CharField(required=False,
                               label="备注",
                               widget=forms.Textarea(attrs={'placeholder': '输入备注'}),
                               )

    class Meta:
        model = PaymentOrder
        fields = ('amount', 'comments')

    def clean(self):
        amount = self.cleaned_data["amount"]
        if amount < 0:
            self.add_error('amount', '收款金额必须大于0')
            raise forms.ValidationError("收款金额必须大于0")


    def save(self, shipment_order, handle, commit=True):
        amount = self.cleaned_data["amount"]
        shipment_order.payable = shipment_order.totalPrice - shipment_order.paid_price
        payment_order_form = super(PaymentOrderCreationForm, self).save(commit=False)
        payment_order_form.shipment_order = shipment_order
        payment_order_form.payment_date = datetime.datetime.now().strftime("%Y-%m-%d")
        payment_order_form.amount = self.cleaned_data["amount"]
        payment_order_form.comments = self.cleaned_data["comments"]
        payment_order_form.handle = handle
        if commit:
            payment_order_form.save()
        return payment_order_form