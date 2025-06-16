from django import forms
from .models import AutoModel

class AutoModelForm(forms.ModelForm):
    YEAR_CHOICES = [(year, year) for year in range(1900, 2027)]

    year = forms.TypedChoiceField(
        choices=YEAR_CHOICES,
        coerce=int,
        required=False,
        label='Pagaminimo metai'
    )

    class Meta:
        model = AutoModel
        fields = '__all__'
