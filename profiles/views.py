from django.shortcuts import render
from .forms import QueryForm


def index(request):
    form = QueryForm()
    context = {'form': form}
    return render(request, 'index.html', context)


def query(request):
    context = {}
    form = QueryForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        print(data)
        searchquery = 'data'
        searchurl = 'https://www.facebook.com/search/' + searchquery + 'intersect/'
        context = {'searchurl': searchurl}
    return render(request, 'result.html', context)
