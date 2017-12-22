from django import forms
from ShipmentOrder.models import ShipmentOrder, Goods
from Customers.models import Customer


class CustomerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.customer_name


class OrderCreationOneForm(forms.ModelForm):
    # 客户
    query_list = Customer.objects.all()
    customer = CustomerChoiceField(queryset=query_list,
                                   required=False,
                                   widget=forms.Select(),
                                   label="客户（可留空）",
                                   )
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
        fields = ("customer", "sender", "from_address", "sender_contact", "receiver", "to_address",
                  "receiver_contact", "mode", "comments",)

    def save(self, commit=True):
        order_form = super(OrderCreationOneForm, self).save(commit=False)
        order_form.customer = self.cleaned_data["customer"]
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
    weight = forms.FloatField(required=True,
                              label="重量",
                              widget=forms.NumberInput(attrs={'placeholder': '输入货物重量'}),
                              error_messages={'required': '此为必填项目'})
    unit_price = forms.FloatField(required=True,
                                  label="运费单价",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入运费单价'}),
                                  error_messages={'required': '此为必填项目'})

    class Meta:
        model = Goods
        fields = ("goods_name", "amount", "weight", "unit_price")

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
    packingFee = forms.FloatField(required=True,
                                  label="包装费",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入包装费用'}),
                                  error_messages={'required': '此为必填项目'})
    claimed_value = forms.FloatField(required=True,
                                  label="声明价值",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入货品声明价值'}),
                                  error_messages={'required': '此为必填项目'})
    insurance_rate = forms.FloatField(required=True,
                                  label="保价率",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入保价率'}),
                                  error_messages={'required': '此为必填项目'})
    volume = forms.FloatField(required=True,
                              label="体积",
                              widget=forms.NumberInput(attrs={'placeholder': '输入货物体积'}),
                              error_messages={'required': '此为必填项目'})
    paymentOnAccountFreight = forms.FloatField(required=True,
                                               label="垫货运费",
                                               widget=forms.NumberInput(attrs={'placeholder': '输入已垫付费用'}),
                                               error_messages={'required': '此为必填项目'})

    class Meta:
        model = ShipmentOrder
        fields = ("packingFee", "claimed_value", "insurance_rate", "paymentOnAccountFreight", "volume")

    def save(self, commit=True):
        order_form = super(OrderCreationThreeForm, self).save(commit=False)
        order_form.packingFee = self.cleaned_data["packingFee"]
        order_form.paymentOnAccountFreight = self.cleaned_data["paymentOnAccountFreight"]
        order_form.volume = self.cleaned_data["volume"]
        if commit:
            order_form.save()
        return order_form


class OrderModityForm(forms.ModelForm):
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

    # 费用
    packingFee = forms.FloatField(required=True,
                                  label="包装费",
                                  widget=forms.NumberInput(attrs={'placeholder': '输入包装费用'}),
                                  error_messages={'required': '此为必填项目'})
    claimed_value = forms.FloatField(required=True,
                                     label="声明价值",
                                     widget=forms.NumberInput(attrs={'placeholder': '输入货品声明价值'}),
                                     error_messages={'required': '此为必填项目'})
    insurance_rate = forms.FloatField(required=True,
                                      label="保价率",
                                      widget=forms.NumberInput(attrs={'placeholder': '输入保价率'}),
                                      error_messages={'required': '此为必填项目'})
    volume = forms.FloatField(required=True,
                              label="体积",
                              widget=forms.NumberInput(attrs={'placeholder': '输入货物体积'}),
                              error_messages={'required': '此为必填项目'})
    paymentOnAccountFreight = forms.FloatField(required=True,
                                               label="垫货运费",
                                               widget=forms.NumberInput(attrs={'placeholder': '输入已垫付费用'}),
                                               error_messages={'required': '此为必填项目'})

    class Meta:
        model = ShipmentOrder
        fields = ("sender", "from_address", "sender_contact", "receiver", "to_address",
                  "receiver_contact", "mode", "comments", "packingFee", "claimed_value", "insurance_rate", "packingFee",
                  "claimed_value", "insurance_rate", "paymentOnAccountFreight", "volume")

    def save(self, commit=True, insurance=0, freight=0):
        order_form = super(OrderModityForm, self).save(commit=False)
        order_form.sender = self.cleaned_data["sender"]
        order_form.from_address = self.cleaned_data["from_address"]
        order_form.sender_contact = self.cleaned_data["sender_contact"]
        order_form.receiver = self.cleaned_data["receiver"]
        order_form.to_address = self.cleaned_data["to_address"]
        order_form.receiver_contact = self.cleaned_data["receiver_contact"]
        order_form.mode = self.cleaned_data["mode"]
        order_form.comments = self.cleaned_data["comments"]
        order_form.packingFee = self.cleaned_data["packingFee"]
        order_form.paymentOnAccountFreight = self.cleaned_data["paymentOnAccountFreight"]
        order_form.volume = self.cleaned_data["volume"]
        order_form.claimed_value = self.cleaned_data["claimed_value"]
        order_form.insurance_rate = self.cleaned_data["insurance_rate"]
        order_form.totalPrice = insurance + freight + float(order_form.packingFee) \
                                - float(order_form.paymentOnAccountFreight)
        if commit:
            order_form.save()
        return order_form




