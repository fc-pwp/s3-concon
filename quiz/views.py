from django.shortcuts import render
from django.shortcuts import redirect
from django import forms

from .models import Quiz


class StartQuizForm(forms.Form):
    username = forms.CharField(label='이름은?', min_length=2)


def toppage(request):
    ctx = {
        'title': '우주 최강 퀴즈 서비스, 콩콩!',
        'welcome_message': '환영합니다. 퀴즈를 즐겨보세요.',
    }
    return render(request, 'toppage.html', ctx)


def list_quiz(request):
    try:
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError, ):
        page = 1

    per_page = 2
    start = (page - 1) * per_page
    end = page * per_page

    contents = Quiz.objects.all().order_by('-updated')
    contents = contents[start:end]

    ctx = {
        'quizzes': contents,
        'page': page,
        # 'page': request.GET['page'],
    }
    return render(request, 'list_quiz.html', ctx)


def start_quiz(request, pk):
    quiz_info = Quiz.objects.get(pk=pk)

    if request.method == 'GET':
        quizform = StartQuizForm()
    elif request.method == 'POST':
        quizform = StartQuizForm(request.POST)
        if quizform.is_valid():
            url = '/quiz/{pk}/questions/1/'.format(pk=quiz_info.pk)
            return redirect(url)

    ctx = {
        'form': quizform,
        'quiz': quiz_info,
    }
    return render(request, 'start_quiz.html', ctx)
