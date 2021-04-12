# from math import ceil
from django.http import HttpResponseRedirect
from django.shortcuts import render
from board import models

LIST_COUNT = 10


def index(request):
    results = models.listall()
    data = {'post_list': results}

    page = request.GET.get('p')
    page = 1 if page is None else int(page)

    print(page)

    '''
    page = request.GET['p']

    totalcount = models.count()
    boardlist = models.findall(page, LIST_COUNT)

    # paging 정보 계산
    pagecount = ceil(totalcount / LIST_COUNT)

    data = {
        "boardlist": boardlist,
        "pagecount": pagecount,
        "netpage": 7,
        "prvpage": 5,
        "curpage": 2,
    }
    '''
    return render(request, 'board/index.html', data)


def view(request):
    no = request.GET['no']
    result = models.listbyno(no)
    data = {'result': result}
    return render(request, 'board/view.html', data)


def writeform(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/user/loginform?sendto=writeform')

    return render(request, 'board/writeform.html')


def write(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/user/loginform?sendto=writeform')

    user_no = authuser['no']
    title = request.POST['title']
    contents = request.POST['content']
    models.insert_new_post(title, contents, user_no)
    return HttpResponseRedirect('/board')


def updateform(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    no = request.GET['no']
    result = models.listbyno(no)
    if result['bno'] != authuser['no']:  # 비정상 로그인일 때.
        return HttpResponseRedirect('/')

    data = {'result': result}
    return render(request, 'board/updateform.html', data)


def update(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    ano = request.POST['post_id']
    result = models.listbyno(ano)
    if result['bno'] != authuser['no']:  # 비정상 로그인일 때 메인으로.
        return HttpResponseRedirect('/')
    title = request.POST['title']
    contents = request.POST['contents']

    models.update(ano, title, contents)
    return HttpResponseRedirect(f'/board/view?no={ano}')


def deleteform(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    no = request.GET['no']
    result = models.listbyno(no)
    if result['bno'] is not authuser['no']:  # 비정상 로그인일 때.
        return HttpResponseRedirect('/')

    return render(request, 'board/deleteform.html')


# 이게 문제. result fail시 MultiValueDictKeyError 에러뜸.
def delete(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    no = request.POST['post_id']
    result = models.listbyno(no)
    if result['bno'] != authuser['no']:  # 비정상 로그인일 때.
        return HttpResponseRedirect('/')

    password = request.POST['password']
    user_id = models.findby_no_and_pw(no, password)
    if user_id is None:
        return HttpResponseRedirect(f'/board/deleteform?no={no}&result=fail')

    models.deleteby_no(no)

    return HttpResponseRedirect('/board')



def replyform(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    return render(request, 'board/replyform.html')


def reply(request):
    authuser = request.session.get('authuser')  # 로그인이 안된 상태에서의 접근인지 확인.
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    user_no = authuser['no']        # 'no' = user_no
    ano = request.POST['post_id']
    result = models.listbyno(ano)
    title = request.POST['title']
    contents = request.POST['content']
    g_no = result['g_no']
    depth = result['depth'] + 1
    models.insert_reply(title, contents, g_no, depth, user_no)
    return HttpResponseRedirect('/board')



