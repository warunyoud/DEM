from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.db.models import Q 

from .forms import LoginForm
from accounts.forms import RegisterForm
from accounts.models import MyUser, UserProfile
@login_required(login_url = '/login/')
def home(request):
	obj = request.user
	context = {
		"user": obj,
	}
	return render(request, "new_home.html", context)

def search_users(request):
	query = request.GET['q']

	qs = UserProfile.objects.all()
	for term in query.split():
		qs = qs.filter( Q(user__first_name__icontains = term) | Q(user__last_name__icontains = term) | Q(user__username__icontains=query))
	objs = qs
	objs = objs.exclude(user__username = request.user.username)
	html = "search_users.html"

	context = {
		'objs': objs,
		'query': query
	}
	return render(request, html, context)


def auth_logout(request):
	logout(request)
	return HttpResponseRedirect('/')


def auth_login(request):
	login_form = LoginForm(request.POST or None)
	if(login_form.is_valid()):
		username = login_form.cleaned_data['username']
		password = login_form.cleaned_data['password']
		user =  authenticate(username = username, password = password)
		if (user is not None):
			login(request, user)
			return HttpResponseRedirect('/')

	context = {
		"login_form": login_form
	}
	return render(request,"login.html", context)

@login_required(login_url = '/staff/login/')
def staff(request):
	return render(request, "base.html", {})



