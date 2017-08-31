from django import forms
from order.models import Item


class HomeForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Search item ...'
        }
    ))

    class Meta:
        model = Item
        fields = ('title',)
