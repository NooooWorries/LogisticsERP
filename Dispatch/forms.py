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


