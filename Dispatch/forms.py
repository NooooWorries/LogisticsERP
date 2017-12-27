from django import forms
from Dispatch.models import Driver, DispatchRecord


class DriverCreationForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           label="司机姓名",
                           widget=forms.TextInput(attrs={'placeholder': '输入司机姓名'}),
                           error_messages={'required': '此为必填项目'}
                           )
    identity_number = forms.CharField(
                           label="身份证号",
                           widget=forms.TextInput(attrs={'placeholder': '输入身份证号（非必须）'}),
                           )
    birthday = forms.DateField(required=True,
                               label="出生日期",
                               widget=forms.TextInput(attrs={'placeholder': '出生日期', ' data-am-datepicker':'', 'readonly':''}),
                               error_messages={'required': '此为必填项目'}
                               )
    license = forms.CharField(required=True,
                              label="驾照号码",
                              widget=forms.TextInput(attrs={'placeholder': '输入驾照号码'}),
                              error_messages={'required': '此为必填项目'}
                              )
    comments = forms.CharField(required=False,
                               label="备注",
                               widget=forms.Textarea(attrs={'placeholder': '输入备注'}),
                               )

    class Meta:
        model = Driver
        fields = ('name', 'identity_number', 'birthday', 'license', 'comments')

    def save(self, commit=True):
        driver_form = super(DriverCreationForm, self).save(commit=False)
        driver_form.name = self.cleaned_data["name"]
        driver_form.identity_number = self.cleaned_data["identity_number"]
        driver_form.birthday = self.cleaned_data["birthday"]
        driver_form.license = self.cleaned_data["license"]
        driver_form.comments = self.cleaned_data["comments"]
        if commit:
            driver_form.save()
        return driver_form


class DriverChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class DispatchRecordCreationForm(forms.ModelForm):
    query_list = Driver.objects.all()
    driver = DriverChoiceField(queryset=query_list,
                                       required=True,
                                       widget=forms.Select(),
                                       label="司机",
                                       )
    vehicle_number = forms.CharField(required=True,
                                     label="车牌号",
                                     widget=forms.TextInput(attrs={'placeholder': '输入运输车辆的车牌号'}),
                                     error_messages={'required': '此为必填项目'}
                                     )
    dispatch_date = forms.DateField(required=True,
                                    label="发车日期",
                                    widget=forms.TextInput(attrs={'placeholder': '选择发车日期', ' data-am-datepicker': '', 'readonly': ''}),
                                    error_messages={'required': '此为必填项目'}
                                    )
    origin = forms.CharField(required=True,
                             label="发出地",
                             widget=forms.TextInput(attrs={'placeholder': '输入发出地'}),
                             error_messages={'required': '此为必填项目'}
                             )
    destination = forms.CharField(required=True,
                                  label="到达地",
                                  widget=forms.TextInput(attrs={'placeholder': '输入到达地'}),
                                  error_messages={'required': '此为必填项目'}
                                  )
    comments = forms.CharField(required=False,
                               label="备注",
                               widget=forms.Textarea(attrs={'placeholder': '输入备注'}),
                               )

    class Meta:
        model = DispatchRecord
        fields = ('driver', 'vehicle_number', 'dispatch_date', 'origin', 'destination', 'comments')

    def save(self, commit=True):
        dispatch_record_form = super(DispatchRecordCreationForm, self).save(commit=False)
        dispatch_record_form.driver = self.cleaned_data["driver"]
        dispatch_record_form.vehicle_number = self.cleaned_data["vehicle_number"]
        dispatch_record_form.dispatch_date = self.cleaned_data["dispatch_date"]
        dispatch_record_form.origin = self.cleaned_data["origin"]
        dispatch_record_form.destination = self.cleaned_data["destination"]
        dispatch_record_form.comments = self.cleaned_data["comments"]
        if commit:
            dispatch_record_form.save()
        return dispatch_record_form
