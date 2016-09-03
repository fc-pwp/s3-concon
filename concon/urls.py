from django.conf.urls import url
from django.contrib import admin

from quiz.views import toppage


urlpatterns = [
    url(r'^$', toppage),
    url(r'^admin/', admin.site.urls),
]
