# myapp/forms.py
from django import forms
from django.core.exceptions import ValidationError

class CodeForm(forms.Form):
    codes = forms.CharField(
        label='Enter Codes (space-separated)',
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter multiple 8-character codes separated by spaces',
            'class': 'form-control',
            'rows': 3
        }),
        help_text='Enter multiple 8-character codes separated by spaces'
    )
