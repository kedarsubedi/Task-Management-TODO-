from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class UserProfileForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username...'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your email...'}),
        }
    # add class to form fields
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a password...'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})
        for field in self.fields:
            if not field == 'is_active':
                self.fields[field].widget.attrs.update({
                    'class':'form-control'
                })

class ResetPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        field = '__all__'
    field_order=['old_password', 'new_password1', 'new_password2']
    
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if not field == 'is_active':
                self.fields[field].widget.attrs.update({
                    'class':'form-control'
                })
    