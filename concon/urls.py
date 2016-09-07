from django.conf.urls import url
from django.contrib import admin

from quiz.views import toppage
from quiz.views import list_quiz


urlpatterns = [
    # url(r'^list/$', list_quiz),  # /list/
    url(r'^$', list_quiz),
    # url(r'^$', toppage),
    url(r'^admin/', admin.site.urls),
]
