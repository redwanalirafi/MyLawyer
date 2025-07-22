from django import forms
from .models import *

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
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class LawyerProfileForm(forms.ModelForm):
    class Meta:
        model = LawyerProfile
        fields = ['profile_picture', 'specialization', 'experience_years', 'bio', 'available']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProfileStatusForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 10, 
                'placeholder': 'Write your report here...'
            })
        }