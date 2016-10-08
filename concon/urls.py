from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from quiz.views import toppage
from quiz.views import list_quiz
from quiz.views import start_quiz
from quiz.views import view_question


urlpatterns = [
    url(r'^quiz/(?P<pk>[0-9]+)/$', start_quiz), # /quiz/1/
    # quiz/6/questions/1/
    url(r'quiz/(?P<pk>[0-9]+)/questions/(?P<seq>[0-9]+)/$', view_question),
    # url(r'^list/$', list_quiz),  # /list/
    url(r'^$', list_quiz),
    # url(r'^$', toppage),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
