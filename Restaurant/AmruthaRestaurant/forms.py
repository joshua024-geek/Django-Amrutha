from django import forms
from .models import MenuItem

class SignUpForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Full Name',
            'id': 'fullname'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'E-mail',
            'id': 'email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'id': 'password'
        })
    )
    copassword = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'id': 'copassword'
        })
    )

class SignInForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'E-mail',
            'id': 'email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'id': 'password'
        })
    )
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image']
        labels = {
            'name': 'Food Name',
            'description': 'Description',
            'price': 'Price (in USD)',
            'image': 'Food Image'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'style': 'width: 350px;'}),
        }
