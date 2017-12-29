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
        searchquery = utils.get_searchquery(data)
        searchurl = 'https://www.facebook.com/search/' + searchquery + 'intersect/'
        utils.login_facebook('lizzethcamargo@hotmail.com', 'lasquierobreggethmaria79')
        limit = int(data['limit']) if data['limit'] else None
        profiles = utils.get_data_profiles_search(searchurl, limit)
        utils.save_profiles(profiles)
        utils.close_bot()
        context = {'searchurl': searchurl, 'profiles': profiles}
    return render(request, 'result.html', context)
