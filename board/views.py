from django.http import HttpResponseRedirect
from django.shortcuts import render
from board import models


def index(request):
    #results = models.findall()
    #data = {'guestbook_list': results}
    #return render(request, 'guestbook/index.html', data)
    return render(request, 'board/index.html')
