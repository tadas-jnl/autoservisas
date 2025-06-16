from django import forms
from .models import AutoModel

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
