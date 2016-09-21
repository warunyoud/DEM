from django.shortcuts import render, Http404, HttpResponseRedirect, HttpResponse
from .models import MyUser, UserProfile
from django.db.models import Q 
import json


#from notifications.signals import notify
from django.contrib.auth import get_user

""" General Function """
def get_connect_status(request, obj):
	#not 
	connect_status = 0

	if not request.user.is_authenticated():
		connect_status = -2

	elif(request.user == obj):
		#same person
		connect_status = -1
	# if hasattr(obj.profile.user, "my_notifications"):
	elif len(request.user.my_notifications.filter(sender = obj).filter(notification_type = 'CNT')) != 0:
		#you just need to accept
		connect_status = 1
	elif len(obj.my_notifications.filter(sender = request.user).filter(notification_type = 'CNT')) != 0:
		#waiting for response
		connect_status = 2
	elif obj.profile in request.user.profile.connections.all():
		connect_status = 3
	return connect_status

""" View Functions """
def account_detail(request, slug):
	obj = MyUser.objects.get(slug = slug)
	connect_status = get_connect_status(request, obj)
	context = {
		"profile": obj.profile,
		"connect_status": connect_status
	}
	return render(request, "user_detail.html", context)


def account_cancel_request(request, slug):
	try:
		obj = MyUser.objects.get(slug = slug)
		if hasattr(request.user, "my_notifications") and len(obj.my_notifications.filter(notification_type = 'CNT').filter(sender = request.user)) != 0:
			obj.my_notifications.filter(notification_type = 'CNT').get(sender = request.user).delete()
			return HttpResponseRedirect('/users/' + slug)
		else:
			raise Http404
	except:
		raise Http404
	
def doctor_cancel_request(request, slug):
	try:
		obj = MyUser.objects.get(slug = slug)
		if hasattr(request.user, "my_notifications") and len(obj.my_notifications.filter(sender = request.user)) != 0:
			obj.my_notifications.get(sender = request.user).delete()
			return HttpResponseRedirect('/doctors/' + slug)
		else:
			raise Http404
	except:
		raise Http404

def get_user_suggestion_ajax(request):
	if request.is_ajax():
		query = request.POST.get("slug")
		qs = request.user.profile.connections.all()
		for term in query.split():
			qs = qs.filter( Q(user__first_name__icontains = term) | Q(user__last_name__icontains = term) | Q(user__username__icontains=query))
		objs = qs
		objs = objs.exclude(user__username = request.user.username)

		selected = request.POST.getlist("selected[]")

		if selected:
			for user in selected:
				terms = user.split()
				objs = objs.exclude(user__first_name = terms[0], user__last_name = terms[1])

		objs = objs[:5]

		suggestions = []
		users = []
		i = 0
		for obj in objs:
			suggestions.append('<li class="list-group-item" id = "user' + str(i) + '"><div class="media"><a class="media-left" href="#asdf"><img class="media-object img-circle" src='+obj.image_url+'></a><div class="media-body"><strong>'+obj.full_name+' </strong><small> @' + obj.user.username +' - San Francisco</small></div></div></li>')
			users.append(obj.full_name)
			i += 1

		data = {
			'suggestions': suggestions,
			'users': users
		}

		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404
