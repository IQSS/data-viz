from django.shortcuts import render, render_to_response
from django.http import HttpResponse

def view_hello(request, name='cathy'):

    #return HttpResponse('hello: ' + name)

    d = dict(name=name)  # same as { 'name' : name }

    return render_to_response('hello.html', d)
