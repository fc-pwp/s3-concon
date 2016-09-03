from django.shortcuts import render


def toppage(request):
    ctx = {
        'title': '우주 최강 퀴즈 서비스, 콩콩!',
        'welcome_message': '환영합니다. 퀴즈를 즐겨보세요.',
    }
    return render(request, 'toppage.html', ctx)
