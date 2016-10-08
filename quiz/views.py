from django.shortcuts import render
from django.shortcuts import redirect
from django import forms

from .models import Quiz
from .models import Question
from .models import Answer
from .models import UserScore


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


def view_question(request, pk, seq):
    # pk = Quiz의 기본키(pk)
    # seq = Question의 순번(sequence)
    seq = int(seq)
    quiz_info = Quiz.objects.get(id=pk)
    # question_info = Question.objects.get(퀴즈=6번퀴즈, 순번=1)
    question_info = Question.objects.get(quiz=quiz_info, sequence=seq)
    has_next = Question.objects \
        .filter(quiz=quiz_info, sequence=seq+1).exists()

    answer_list = Answer.objects \
        .filter(question=question_info).order_by('sequence')

    if request.method == 'POST':
        answer_seq = request.POST['sequence']  # html input 태그의 name 속성 값
        user_answer = Answer.objects \
            .get(question=question_info, sequence=answer_seq)

        score = UserScore()
        score.quiz = quiz_info
        score.answer = user_answer
        score.session_key = request.session.session_key
        score.save()

        if has_next:
            url = '/quiz/{pk}/questions/{seq}/'.format(
                pk=quiz_info.pk,
                seq=question_info.sequence + 1,
            )
            return redirect(url)

    ctx = {
        'quiz': quiz_info,
        'question': question_info,
        'answers': answer_list,
        'has_next': has_next,
    }
    return render(request, 'view_question.html', ctx)
