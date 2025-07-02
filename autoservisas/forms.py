from django import forms
from .models import AutoModel, Comment, Profile, OrderData, Auto, OrderLine
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class AutoModelForm(forms.ModelForm):
    YEAR_CHOICES = [(year, year) for year in range(2025, 1900, -1)]
    #(year, year) nes ChoiceField reikalauja tuple (value, label)
    year = forms.TypedChoiceField(
        choices=YEAR_CHOICES,
        required=False,
        label='Pagaminimo metai'
    )

    class Meta:
        model = AutoModel
        fields = '__all__'

class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='El. paštas',
                             widget=forms.EmailInput(attrs={'type': 'email'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"{email} is taken.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = OrderData
        fields =['auto']
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Pull user from kwargs
        super().__init__(*args, **kwargs)
        self.fields['auto'].queryset = Auto.objects.filter(owner=user)

class ManageOrderForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=OrderData.ORDER_STATUS,
        label='Būsena',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = OrderData
        fields = ['status', 'deadline']

        widgets = {
            'deadline': DateTimePickerInput(
                options={
                    "format": "YYYY-MM-DD HH:mm",
                    "stepping": 15,  # ⏰ optional: sets time interval (15 mins)
                    "useCurrent": True,
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                    "sideBySide": True  # ✅ shows date & time picker next to each other
                }
            )
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # 👈 pull user from kwargs
        super().__init__(*args, **kwargs)

class CreateOrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ['order_data', 'service', 'qty']
        widgets = {
            'order_data': forms.HiddenInput()
        }



