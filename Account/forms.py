from django import forms
from django.contrib.auth.models import User
from Account.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': '用户名'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': '密码'}))


class UserCreationForm(UserCreationForm):
    username = forms.CharField(required=True,
                               label="用户名",
                               widget=TextInput(attrs={'class': 'validate', 'placeholder': '用户名'}),
                               error_messages={'required': '此为必填项目'})
    password1 = forms.CharField(required=True,
                                label="密码",
                                widget=PasswordInput(attrs={'placeholder': '输入密码'}),
                                error_messages={'required': '此为必填项目'})
    password2 = forms.CharField(required=True,
                                label="确认密码",
                                widget=PasswordInput(attrs={'placeholder': '验证刚刚输入的密码'}),
                                error_messages={'required': '此为必填项目'})

    email = forms.CharField(required=True,
                            label="邮箱",
                            widget=forms.TextInput(attrs={'placeholder': '输入邮箱地址'}),
                            error_messages={'required': '此为必填项目'}
                            )
    last_name = forms.CharField(required=True,
                                label="姓",
                                widget=forms.TextInput(attrs={'placeholder': '输入姓'}),
                                error_messages={'required': '此为必填项目'}
                                )
    first_name = forms.CharField(required=True,
                                 label="名",
                                 widget=forms.TextInput(attrs={'placeholder': '输入名'}),
                                 error_messages={'required': '此为必填项目'}
                                 )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "last_name", "first_name")

    def save(self, commit=True):
        user_form = super(UserCreationForm, self).save(commit=False)
        user_form.email = self.cleaned_data["email"]
        user_form.last_name = self.cleaned_data["last_name"]
        user_form.first_name = self.cleaned_data["first_name"]

        if commit:
            user_form.save()
        return user_form


class UserProfileCreationForm(forms.ModelForm):
    ROLE_CHOICE = (
        (0, "管理员"),
        (1, "入库员"),
        (2, "文员"),
        (3, "司机"),
        (4, "财务"),
    )
    GENDER_CHOICE = (
        (True, "男"),
        (False, "女"),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICE,
                             label="角色",
                             error_messages={'required': '此为必选项目'}
                             )
    gender = forms.ChoiceField(choices=GENDER_CHOICE,
                               label="性别",
                               error_messages={'required': '此为必选项目'}
                               )
    birthday = forms.DateField(required=False,
                               label="出生日期",
                               widget=forms.TextInput(
                                   attrs={'placeholder': '出生日期', ' data-am-datepicker': '', 'readonly': ''}),
                               )
    comments = forms.CharField(required=False,
                               label="备注",
                               widget=forms.Textarea(attrs={'placeholder': '输入备注'}),
                               )

    class Meta:
        model = UserProfile
        fields = ("role", "gender", "birthday", "comments")
        exclude = ['id']

    def save(self, commit=True):
        user_profile_form = super(UserProfileCreationForm, self).save(commit=False)
        user_profile_form.role = self.cleaned_data["role"]
        user_profile_form.gender = self.cleaned_data["gender"]
        user_profile_form.birthday = self.cleaned_data["birthday"]
        user_profile_form.comments = self.cleaned_data["comments"]

        if commit:
            user_profile_form.save()
        return user_profile_form
