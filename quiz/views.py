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

    ctx = {
        'quizzes': quizzes,
    }
    return render(request, 'list_quiz.html', ctx)
