from django.contrib import admin

from .models import Quiz
from .models import Question


class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'updated']
    list_display_links = ['id', 'title', ]
    search_fields = ['title']

admin.site.register(Quiz, QuizAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'updated']
    list_display_links = ['id', 'title', ]
    search_fields = ['title']
    list_filter = ['quiz', 'sequence']

admin.site.register(Question, QuestionAdmin)
