# views/auth.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
#from ..models import UserProfile  # Change this line

#class CustomSignupView(SignupView):
#    def form_valid(self, form):
#        response = super().form_valid(form)
#        UserProfile.objects.create(user=self.request.user)  # Create a UserProfile for the new user
#        return response

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "auth/signup.html", {"form": form})

class LoginView(BaseLoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True

login = LoginView.as_view()

