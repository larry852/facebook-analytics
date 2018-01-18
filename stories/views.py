from django.shortcuts import render
from . import utils


def index(request):
    return render(request, 'stories/index.html')


def query(request):
    context = {}
    data = request.POST
    print(utils.main(data))
    return render(request, 'stories/result.html', context)
