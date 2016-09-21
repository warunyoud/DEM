"""DEM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from .views import *
from notifications.views import *
from accounts.views import *
# from chat.views import *

urlpatterns = [
    url(r'^$', home, name='home'),

    # url(r'^about/$', about, name = 'about'),
	# url(r'^staff/$', staff, name= 'staff'),
    url(r'^login/$', auth_login, name='login'),
    url(r'^logout/$', auth_logout, name='logout'),

    #search
    url(r'^search/users/$', search_users, name='search_users'),

    url(r'^users/(?P<slug>[\w-]+)/$', account_detail, name='account_detail'),
    url(r'^req/$', req, name='req'),

    url(r'^users/(?P<slug>[\w-]+)/sendrequest/$', send_request, name='send_request'),
    url(r'^users/(?P<slug>[\w-]+)/remove/$', remove_connection, name='remove_connection'),
    url(r'^users/(?P<slug>[\w-]+)/accept/$', accept_request, name='accept_request'),
    url(r'^users/(?P<slug>[\w-]+)/decline/$', decline_request, name='decline_request'),
    url(r'^users/(?P<slug>[\w-]+)/cancelrequest/$', account_cancel_request, name='account_cancel_request'),

    url(r'^admin/', admin.site.urls),

    #ajax
    url(r'^ajax/getupdates/$', get_updates_ajax, name = 'get_updates_ajax'),
    url(r'^ajax/getrequests/$', get_requests_ajax, name = 'get_requests_ajax'),
    url(r'^ajax/getmessages/$', get_messages_ajax, name = 'get_messages_ajax'),
    url(r'^ajax/getsuggestions/$', get_user_suggestion_ajax, name = 'get_user_suggestion_ajax'),
    url(r'^ajax/createchat/$', create_chat, name = 'create_chat'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

