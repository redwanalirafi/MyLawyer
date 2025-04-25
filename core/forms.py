from django import forms
from .models import HireRequest

class HireRequestForm(forms.ModelForm):
    class Meta:
        model = HireRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Explain your legal situation and why you want to hire this lawyer...'
            })
        }
        labels = {
            'message': 'Your message to the lawyer'
        }