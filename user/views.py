from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from user import models


def joinform(request):
    return render(request, 'user/joinform.html')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def join(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    gender = request.POST['gender']

    models.insert(name, email, password, gender)

    return HttpResponseRedirect("/user/joinsuccess")


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    email = request.POST['email']
    password = request.POST['password']
    sendto = request.POST['sendto']

    result = models.findby_email_and_password(email, password)      # (no, name)에 email, gender를 추가로 넣어줌.
    if result is None:
        return HttpResponseRedirect('/user/loginform?result=fail')
    # login 처리 (cookie; session 사용)
    request.session["authuser"] = result            # DictCursor기 때문에 아마도 dict형으로 받아옴

    # 예) 글쓰기에서 로그인 할 경우, 다시 글쓰기페이지로 보내줌
    if sendto is not '':
        return HttpResponseRedirect(f'/board/{sendto}')

    return HttpResponseRedirect('/')


def logout(request):
    del request.session["authuser"]
    return HttpResponseRedirect('/')


def updateform(request):
    # 접근제어 Access Control
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/')

    # authuser = request.session['authuser']
    # result = models.findbyno(authuser['no'])
    return render(request, 'user/updateform.html')


def update(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태 or 만료된 세션에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/')

    name = request.POST['name']
    password = request.POST['password']
    gender = request.POST['gender']
    no = request.session['authuser']['no']

    models.update(name, password, gender, no)
    request.session['authuser'] = models.findbyno(no)   # 다시 로그인, session_save 설정으로 바로 표현

    return HttpResponseRedirect('/user/updateform')
