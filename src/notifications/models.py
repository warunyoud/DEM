from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from .signals import notify
from django.middleware.csrf import get_token
from accounts.models import MyUser
# Create your models here.

TYPE_CHOICES = (
	('CNT', 'Connect'),
	('MSG', 'Message'),
	('REG', 'Regular'),
)

class Chat(models.Model):
	users = models.ManyToManyField(MyUser, blank = True)

	def get_last_message(self):
		messages = self.message.all().order_by('-timestamp')
		return messages[0]


class Notification(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'sent_notifications')
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'my_notifications')
	action = models.CharField(max_length=255, null = True, blank = True)
	notification_type = models.CharField(max_length = 3, choices = TYPE_CHOICES, default = 'CNT')
	read = models.BooleanField(default = False)
	#read
	#unread
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	chat = models.ForeignKey(Chat, related_name = 'notifications', null = True, blank = True)

	def __str__(self):
		return "blank"

	def get_html(self, request):
		csrf_token = "<input type='hidden' name='csrfmiddlewaretoken' value= " + str(get_token(request)) + ">"
		if self.read:
			new = ""
		else:
			new = "<span class='badge' style = 'background:red;' id = 'messageC'>new!!</span>"

		if self.notification_type == 'CNT':
			return "<a href = '"+ str(self.sender.get_absolute_url()) +"'' class='list-group-item' ><div class='media'><span class='media-left'><img class='img-circle media-object' src =" + str(self.sender.profile.image_url) + "></span><div class='media-body'><li><strong>" + str(self.sender.profile.full_name) + "</strong> " + new + "<div class='media-body-actions pull-right'><form action='/req/' method='POST'> " + csrf_token+ " <input type='hidden' name='slug' value='"+ self.sender.slug +"'><button name = 'action' value = 'accept' type = 'submit' class='btn btn-primary btn-sm'>Connect </button><button name = 'action' value = 'decline' type = 'submit' class='btn btn-primary-outline btn-sm'>Decline </button></form></div></li><div class='media-body-secondary'> I like pizza and you like it too </div></div></div></a>"
		elif self.notification_type == 'MSG':
			chat = self.chat
			html = "<a href='#'' class='list-group-item'><div class='media'><span class='media-left'><img class='img-circle media-object' "
			#put picture here
			html += "src=" + str(self.sender.profile.image_url)

			html += "></span><div class='media-body'>"

			#group or not group
			users =  chat.users.exclude(slug = request.user.slug)
			html += "<strong>"
			#participants
			if len(users) == 1:
				html += users[0].first_name + "</strong>"

				html += "<div class='media-body-secondary'>"
				message = chat.get_last_message()
				html += message.text
				html += " </div></div> </div></a>"
			else:
				for user in users[:2]:
					html += user.first_name + ", "

				html += "</strong>and <strong>1 other</strong>"

				html += "<div class='media-body-secondary'>"

				#message
				message = chat.get_last_message()
				prefix = ""
				if(message.sender != request.user):
					prefix = message.sender.first_name + ": "
				html += prefix + message.text
				html += " </div></div> </div></a>"
			return html




class Message(models.Model):
	sender = models.ForeignKey(MyUser, related_name = "my_message")
	readBy = models.ManyToManyField(MyUser, related_name = "my_read_message", blank = True)
	chat = models.ForeignKey(Chat, related_name = "message")
	text = models.CharField(max_length=255, null = True)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)

def new_notification(sender, recipient, action, notification_type, *args, **kwargs):
	noti = Notification()
	noti.sender = sender
	noti.recipient = recipient
	noti.action = action
	noti.notification_type = notification_type
	noti.save()

notify.connect(new_notification)
