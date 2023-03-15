from django import forms
from django.contrib.auth import get_user_model
from .models import Order, ChangePassword, CommentModel, Support


User = get_user_model()


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = (
            'name', 'generalDescription', 'comment'
        )


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = ChangePassword
        fields = ('login', 'email', 'newPassword')


class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ('name', 'contact', 'description')


class OrderForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['order_date'].label = 'Дата отримання замовлення'
    #
    # order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'comment'
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'користувач с логіном "{username}" не існує!')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неправльний пароль")
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Повторіть пароль'
        self.fields['phone'].label = 'Номер телефону'
        self.fields['email'].label = 'Електронна пошта'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f'Даннай пошта вже зареєстрована'
            )
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f'Логін {username} вже використовується, будь ласка спробуйде інший'
            )
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Паролі не співпадають')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'phone', 'email']


# class ChangePasswordForm(forms.ModelForm):
#
#     oldPassword = forms.CharField(widget=forms.PasswordInput)
#     newPassword = forms.CharField(widget=forms.PasswordInput)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password'].label = 'Старий пароль'
#         self.fields['password'].label = 'Новий пароль'
#         self.fields['confirm_password'].label = 'Повторіть новий пароль'
#
#     def clean(self):
#         password = self.cleaned_data['password']
#         confirm_password = self.cleaned_data['confirm_password']
#         if password != confirm_password:
#             raise forms.ValidationError('Паролі не співпадають')
#         return self.cleaned_data
