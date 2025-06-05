from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class CustomSignupForm(SignupForm):
    """
    Custom signup form extending allauth's SignupForm.
    Adds fields for full name, username, email, and optional profile picture.
    Overrides save() to populate additional user fields.
    """
    full_name = forms.CharField(max_length=30, label='Full Name')
    username = forms.CharField(max_length=30, label='Username')
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)

    def save(self, request):
        """
        Saves the user instance with additional fields from the signup form.
        """
        user = super(CustomSignupForm, self).save(request)
        user.full_name = self.cleaned_data['full_name']
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.save()
        return user
    

class ProfileUpdateForm(forms.ModelForm):
    """
    ModelForm for updating user profile details.
    Allows editing of full name, username, email, and profile picture.
    """
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'profile_picture']