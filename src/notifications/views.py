from django.shortcuts import render, Http404, HttpResponseRedirect, HttpResponse, redirect
import accounts
import json
from .signals import notify
# Create your views here.

from .models import Chat, Message, Notification
from accounts.models import MyUser, UserProfile

# Create your views here.
def create_chat(request):
	selected = request.POST.getlist('selected[]')
	message = request.POST['message']
	#create chat
	newChat = Chat()
	newChat.save()

	if selected:
			for user in selected:
				terms = user.split()
				obj = request.user.profile.connections.filter(user__first_name = terms[0], user__last_name = terms[1])
				newChat.users.add(obj[0].user)
	
	#creating new message
	newMessage = Message(text = message, sender = request.user, chat = newChat)
	newMessage.save()

	newChat.message.add(newMessage)
	newChat.save()

	for user in newChat.users.all():
		noti = Notification(sender = request.user, recipient = user, notification_type = 'MSG', chat = newChat)
		noti.save()

	newChat.users.add(request.user)
	newChat.save()
	noti = Notification(sender = request.user, recipient = request.user, notification_type = 'MSG', chat = newChat, read = True)
	noti.save()
	return HttpResponse("success")


def get_requests_ajax(request):
	if request.is_ajax():
		all_notifications = request.user.my_notifications
		notifications = all_notifications.filter(notification_type = 'CNT')[:5]
		notifications = notifications
		notes = []
		for note in notifications:
			notes.append(str(note.get_html(request)))
			note.read = True
			note.save()


		if len(notifications) == 0:
			notes.append("<a class='list-group-item'> <div class='media'><div class='media-body'><li><strong>You don't have any request</strong></div></div></a>")

		data = {
			"notifications" : notes
		}
		json_data = json.dumps(data)

		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404

def get_messages_ajax(request):
	if request.is_ajax():
		all_notifications = request.user.my_notifications.all().order_by('-timestamp')
		notifications = all_notifications.filter(notification_type = 'MSG')[:5]
		notifications = notifications
		notes = []
		for note in notifications:
			notes.append(str(note.get_html(request)))
			note.read = True
			note.save()


		if len(notifications) == 0:
			notes.append("<a class='list-group-item'> <div class='media'><div class='media-body'><li><strong>You don't have any message</strong></div></div></a>")

		data = {
			"notifications" : notes
		}
		json_data = json.dumps(data)

		return HttpResponse(json_data, content_type='application/json') 
	else:
		raise Http404

def get_updates_ajax(request):
	if request.is_ajax():
		requestC = len(request.user.my_notifications.filter(notification_type = 'CNT').filter(read = False))
		messageC = len(request.user.my_notifications.filter(notification_type = 'MSG').filter(read = False))
		regC = 0

		data = {
			"requestC" : requestC,
			"messageC" : messageC,
			"regularC" : regC
		}
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404

def requestHandler(sender, recipient, action):
	if hasattr(recipient, "my_notifications") and len(recipient.my_notifications.filter(sender = sender).filter(notification_type = 'CNT')) != 0:
		if action == "accept":
			recipient.profile.connections.add(sender.profile)
			#notify that they are connected to each other
		elif action == "decline":
			pass
		recipient.my_notifications.filter(notification_type = 'CNT').get(sender = sender).delete()

def req(request):
	slug = request.POST.get("slug")
	action = request.POST.get("action")

	sender = accounts.models.MyUser.objects.get(slug = slug)
	recipient = request.user

	requestHandler(sender,recipient,action)

	return redirect(accounts.views.account_detail, slug = slug)

def decline_request(request, slug):
	sender = accounts.models.MyUser.objects.get(slug = slug)
	recipient = request.user

	requestHandler(sender,recipient,"decline")
	return redirect(accounts.views.account_detail, slug = slug)

def accept_request(request, slug):
	sender = accounts.models.MyUser.objects.get(slug = slug)
	recipient = request.user

	requestHandler(sender,recipient,"accept")
	return redirect(accounts.views.account_detail, slug = slug)

def send_request(request, slug):
	sender = request.user
	recipient = accounts.models.MyUser.objects.get(slug = slug)

	if not hasattr(recipient, "my_notifications") or len(recipient.my_notifications.filter(sender = sender).filter(notification_type = 'CNT')) == 0:
		obj = accounts.models.MyUser.objects.get(slug = slug)
		notify.send(sender = request.user, recipient = obj, action = '', notification_type = 'CNT')
	return redirect(accounts.views.account_detail, slug = slug)

def remove_connection(request, slug):
	obj = accounts.models.MyUser.objects.get(slug = slug)
	request.user.profile.connections.remove(obj.profile)
	return redirect(accounts.views.account_detail, slug = slug)
