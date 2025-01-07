from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email", "password"]
    
    def save(self, commit = True):
        User = super().save(commit=False)
        User.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            User.save()
        return User
