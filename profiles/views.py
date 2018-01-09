from django.shortcuts import render
from .forms import QueryForm
from . import utils
from core import utils as core_utils


def index(request):
    form = QueryForm()
    context = {'form': form}
    return render(request, 'index.html', context)


def query(request):
    import time
    start_time = time.time()

    context = {}
    form = QueryForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        searchquery = utils.get_searchquery(data)
        searchurl = 'https://www.facebook.com/search/{}intersect/'.format(searchquery)
        core_utils.login_facebook()
        limit = int(data['limit']) if data['limit'] else None
        profiles = core_utils.get_data_search(searchurl, limit)
        list_querys = utils.get_querys(data)
        query = utils.save_query(list_querys)
        utils.save_profiles(profiles, query)
        core_utils.close_bot()
        context = {'searchurl': searchurl, 'profiles': profiles}

        print("Get profiles --- {} seconds ---".format(time.time() - start_time))
    return render(request, 'result.html', context)
