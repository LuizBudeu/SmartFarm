from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def first(request):
    return render(request, 'first.html')

def home(request):
    return render(request, 'home.html')

