from django.shortcuts import render
from .forms import QueryForm
from . import utils


def index(request):
    form = QueryForm()
    context = {'form': form}
    return render(request, 'index.html', context)


def query(request):

    context = {}
    form = QueryForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        context = utils.main(data)
    return render(request, 'result.html', context)
