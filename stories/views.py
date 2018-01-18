from django.shortcuts import render
from . import utils


def index(request):
    return render(request, 'stories/index.html')


def query(request):
    context = {}
    return render(request, 'stories/result.html', context)
