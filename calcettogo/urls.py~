"""calcettogo URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from core import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.Login.as_view()),
    url(r'^match/(\d*\.\d+|\d+)/(\d*\.\d+|\d+)/(\d+)/(\d+)/$', views.MatchList.as_view()),
    url(r'^match/$', views.MatchList.as_view()),
    url(r'^match_detail/(\d+)/(\d*\.\d+|\d+)/(\d*\.\d+|\d+)/$', views.MatchDetail.as_view()),
    url(r'^plays/(\d+)/$', views.MatchPlayersList.as_view()),
    url(r'^plays/$', views.MatchPlayersList.as_view()),
    url(r'^vote/([0-9]+)/$', views.MatchVoteList.as_view()),
    url(r'^vote/$', views.MatchVoteList.as_view()),
    url(r'^vote/([0-9]+)/([0-9]+)/$', views.VoteDetail.as_view()),
    url(r'^user_detail/([0-9]+)/$', views.UserDetail.as_view()),
    url(r'^user_matches/([0-9]+)/(\d*\.\d+|\d+)/(\d*\.\d+|\d+)/([0-9]+)/([0-9]+)/$', views.UserMatchList.as_view()),
    url(r'^user_votes/([0-9]+)/$', views.UserVoteList.as_view()),
    url(r'^feedback/([0-9]+)/$', views.FeedbackList.as_view()),
    url(r'^feedback/$', views.FeedbackList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
