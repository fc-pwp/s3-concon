from django.shortcuts import render
from django.shortcuts import redirect
from django import forms

from .models import Quiz
from .models import Question
from .models import Answer
from .models import UserScore
from .models import Result


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


# http://localhost:8080/quiz/6/questions/1/
def view_question(request, pk, seq):
    previous = request.GET.get('previous')
    if not previous:
        previous = request.POST.get('previous')
    if previous:
        previous_info = UserScore.objects.get(id=previous)
    else:
        previous_info = None
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
        score.session_key = request.session.session_key
        score.quiz = quiz_info
        score.answer = user_answer
        score.previous = previous_info
        score.save()

        if has_next:
            url = '/quiz/{pk}/questions/{seq}/?previous={prev}'.format(
                pk=quiz_info.pk,
                seq=question_info.sequence + 1,
                prev=score.pk,
            )
            return redirect(url)
        else:
            url = '/quiz/{pk}/result/'.format(pk=quiz_info.pk)
            return redirect(url)

    ctx = {
        'quiz': quiz_info,
        'question': question_info,
        'answers': answer_list,
        'has_next': has_next,
    }
    return render(request, 'view_question.html', ctx)


def view_result(request, pk):
    quiz_info = Quiz.objects.get(id=pk)
    session_key = request.session.session_key
    score = UserScore.objects \
                .filter(session_key=session_key, quiz=quiz_info) \
                .order_by('-created').first()

    code = score.answer.code
    answers = {code: 1}

    while True:
        if not score.previous:  # if score.previous is None:
            code = score.answer.code
            if code in answers:
                answers[code] += 1
            else:
                answers[code] = 1
            break
        score = UserScore.objects.get(id=score.previous.pk)
        code = score.answer.code
        if code in answers:
            answers[code] += 1
        else:
            answers[code] = 1

    result_code = sorted(answers, key=answers.get, reverse=True)
    result = Result.objects.get(quiz=quiz_info, code=result_code[0])

    ctx = {
        'result': result,
    }

    return render(request, 'result.html', ctx)
