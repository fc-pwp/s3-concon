from django.contrib import admin

from .models import Quiz


class QuizAdmin(admin.ModelAdmin):
    pass

admin.site.register(Quiz, QuizAdmin)
