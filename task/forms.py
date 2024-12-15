
from django import forms
from django.contrib.auth.forms import UserCreationForm
from task.models import User, Todo

class SignUpForm(UserCreationForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3 rounded-5', 'placeholder':'Password'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3 rounded-5', 'placeholder':'Confirm Password'}), label='')
    
    class Meta:
        
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control rounded-5', 'placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control mb-3 rounded-5', 'placeholder':'Email Address'}),
            'phone': forms.TextInput(attrs={'class':'form-control mb-3 rounded-5', 'placeholder':'Phone Number'}),
        }
        
        labels = {
            'username': '',
            'email': '',
            'phone': ''
        }
        
        help_texts = {
            "username": "Must contain only letters, numbers, hyphens and underscores.",
        }
        
class SignInForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3 rounded-5', 'placeholder':'Username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3 rounded-5', 'placeholder':'Password'}), label='')
    
    
class TodoForm(forms.ModelForm):
    
    class Meta:
        
        model = Todo
        fields = ['title']