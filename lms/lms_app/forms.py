from django import forms
from .models import Book, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=['name']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'})
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'photo_book',
            'photo_author',
            'pages',
            'price',
            'retal_price_day',
            'retal_period',
            'total_rental',
            'status',
            'category',
        
           ]
        widgets ={
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'author': forms.TextInput(attrs={'class':'form-control'}),
            'photo_book': forms.FileInput(attrs={'class':'form-control'}),
            'photo_author': forms.FileInput(attrs={'class':'form-control'}),
            'pages': forms.NumberInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'retal_price_day': forms.NumberInput(attrs={'class':'form-control','id':'rentalprice' }),
            'retal_period': forms.NumberInput(attrs={'class':'form-control','id':'rentaldays'}),
            'total_rental': forms.NumberInput(attrs={'class':'form-control','id':'totalrental'}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),

        }


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)