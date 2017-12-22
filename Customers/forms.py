from django import forms
from Customers.models import CustomerClass, Customer


class CustomerClassCreationForm(forms.ModelForm):
    class_name = forms.CharField(required=True,
                                 label="用户组名",
                                 widget=forms.TextInput(attrs={'placeholder': '输入用户组名'}),
                                 error_messages={'required': '此为必填项目'}
                                 )
    comments = forms.CharField(required=True,
                               label="描述",
                               widget=forms.Textarea(attrs={'placeholder': '输入用户组描述'}),
                               error_messages={'required': '此为必填项目'}
                               )

    class Meta:
        model = CustomerClass
        fields = ("class_name", "comments",)

    def save(self, commit=True):
        class_form = super(CustomerClassCreationForm, self).save(commit=False)
        class_form.class_name = self.cleaned_data["class_name"]
        class_form.comments = self.cleaned_data["comments"]
        if commit:
            class_form.save()
        return class_form


class CustomerClassChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.class_name


class CustomerCreationForm(forms.ModelForm):
    GENDER_CHOICES = (
        (True, "男"),
        (False, "女"),
    )
    query_list = CustomerClass.objects.all()
    customer_class = CustomerClassChoiceField(queryset=query_list,
                                              required=False,
                                              widget=forms.Select(),
                                              label="客户类别",
                                              )
    customer_name = forms.CharField(required=True,
                                    label="客户名",
                                    widget=forms.TextInput(attrs={'placeholder': '输入客户名'}),
                                    error_messages={'required': '此为必填项目'}
                                    )
    contact_person = forms.CharField(required=True,
                                     label="联系人",
                                     widget=forms.TextInput(attrs={'placeholder': '输入联系人'}),
                                     error_messages={'required': '此为必填项目'}
                                     )
    contact_number = forms.CharField(required=True,
                                     label="联系电话",
                                     widget=forms.TextInput(attrs={'placeholder': '输入联系电话'}),
                                     error_messages={'required': '此为必填项目'}
                                     )
    identity_number = forms.CharField(required=False,
                                      label="身份证号码",
                                      widget=forms.TextInput(attrs={'placeholder': '输入身份证号码（可留空）'}),
                                      )
    gender = forms.ChoiceField(required=True,
                               choices=GENDER_CHOICES,

                               error_messages={'required': '此为必填项目'})
    address = forms.CharField(required=True,
                              label="地址",
                              widget=forms.TextInput(attrs={'placeholder': '输入地址'}),
                              error_messages={'required': '此为必填项目'}
                              )
    comments = forms.CharField(required=False,
                               label="备注",
                               widget=forms.Textarea(attrs={'placeholder': '输入备注'}),
                               )

    class Meta:
        model = Customer
        fields = ("customer_class", "customer_name", "contact_person",
                  "contact_number", "identity_number", "gender",
                  "address", "comments", )

    def save(self, commit=True):
        customer_form = super(CustomerCreationForm, self).save(commit=False)
        customer_form.customer_class = self.cleaned_data["customer_class"]
        customer_form.customer_name = self.cleaned_data["customer_name"]
        customer_form.contact_person = self.cleaned_data["contact_person"]
        customer_form.contact_number = self.cleaned_data["contact_number"]
        customer_form.identity_number = self.cleaned_data["identity_number"]
        customer_form.gender = self.cleaned_data["gender"]
        customer_form.address = self.cleaned_data["address"]
        customer_form.comments = self.cleaned_data["comments"]
        if commit:
            customer_form.save()
        return customer_form


