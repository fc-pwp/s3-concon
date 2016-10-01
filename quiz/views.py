from django.shortcuts import render
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
    if request.method == 'GET':
        quizform = StartQuizForm()
    elif request.method == 'POST':
        quizform = StartQuizForm(request.POST)
        if quizform.is_valid():
            raise Exception('잘 됐네. 다음 수업에서 봅시다.')

    quiz_info = {
        'title': '첫 번째 퀴즈입니다!',
        'pk': pk,
    }

    # if request.method == 'POST':
    #     username = request.POST.get('username', '')
    #     if len(username) < 2:
    #         raise Exception('이름은 두 글자 이상 넣으세요.')
    # else:
    #     username = ''
    ctx = {
        'form': quizform,
        'quiz': quiz_info,
        # 'username': username,
    }
    return render(request, 'start_quiz.html', ctx)
