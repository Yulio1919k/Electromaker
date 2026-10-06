from .forms import LoginForm, RegisterForm


def auth_forms(request):
    if request.user.is_authenticated:
        return {}
    return {'login_form': LoginForm(), 'register_form': RegisterForm()}
