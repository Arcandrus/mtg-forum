from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=30, label='Full Name')
    username = forms.CharField(max_length=30, label='Username')
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.full_name = self.cleaned_data['full_name']
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.save()
        return user
    

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'profile_picture']