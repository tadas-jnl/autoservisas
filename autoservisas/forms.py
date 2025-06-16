from django import forms
from .models import AutoModel

class AutoModelForm(forms.ModelForm):
    YEAR_CHOICES = [(year, year) for year in range(2027, 1900, -1)]  #(year, year) nes ChoiceField reikalauja tuple (value, label)

    year = forms.TypedChoiceField(
        choices=YEAR_CHOICES,
        coerce=int,
        required=False,
        label='Pagaminimo metai'
    )

    class Meta:
        model = AutoModel
        fields = '__all__'
