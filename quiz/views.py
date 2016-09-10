from django.shortcuts import render


def toppage(request):
    ctx = {
        'title': '우주 최강 퀴즈 서비스, 콩콩!',
        'welcome_message': '환영합니다. 퀴즈를 즐겨보세요.',
    }
    return render(request, 'toppage.html', ctx)


def list_quiz(request):
    quizzes = [
        {
            'image': '404.png',
            'title': '첫 번째 퀴즈',
            'message': '퀴즈 소개 메시지',
        },
        {
            'image': '404.png',
            'title': '두 번째 퀴즈',
            'message': '2번 퀴즈 소개 메시지',
        },
    ]





    try:
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError, ):
        page = 1

    # page int
    if True:  # 뭔가 거창한 조건이 있지만, 현실은 걍 True.
        page = page + 1
    # request.POST.get('title', '빈 제목')
    # if 'page' in request.GET:
    #     page = request.GET['page']
    # else:
    #     page = 1

    ctx = {
        'quizzes': quizzes,
        'page': page,
        # 'page': request.GET['page'],
    }
    return render(request, 'list_quiz.html', ctx)


def start_quiz(request, pk):
    quiz_info = {
        'title': '첫 번째 퀴즈입니다!',
        'pk': pk,
    }
    ctx = {
        'quiz': quiz_info,
    }
    return render(request, 'start_quiz.html', ctx)
