from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address')
    newsletter = forms.ChoiceField(
        label='Would you like to be signed up to the Electromaker newsletter?',
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect, initial='no')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''
        for n, p in [('username', 'Enter a username'), ('email', 'Email address'),
                     ('password1', 'Password'), ('password2', 'Confirm password')]:
            self.fields[n].widget.attrs['placeholder'] = p

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(placeholder='Email address', autofocus=False)
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
