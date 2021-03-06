from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from auth import forms
from django.contrib.auth import login
# Create your views here.


class Login(LoginView):
	template_name = 'auth/login.html'

	def get_success_url(self):
		return '/'


class Logout(LogoutView):
	next_page = '/auth/login'

class Signup(View):

	def get(self, request):

		context = {
			"form": forms.SignUpForm()
		}

		return render(request, 'auth/signup.html', context)

	def post(self, request):
		form = forms.SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/')

		else:
			context = {
				'form': form
			}

			return render(request, 'auth/signup.html', context)
