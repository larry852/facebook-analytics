from django.shortcuts import render
from .forms import QueryForm
from .SeleniumHelper import SeleniumHelper

sh = SeleniumHelper()


def index(request):
    form = QueryForm()
    context = {'form': form}
    return render(request, 'index.html', context)


def query(request):
    context = {}
    form = QueryForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        searchquery = get_searchquery(data)
        searchurl = 'https://www.facebook.com/search/' + searchquery + 'intersect/'
        login('lizzethcamargo@hotmail.com', 'lasquierobreggethmaria79')
        print(get_html(searchurl))
        context = {'searchurl': searchurl}
    return render(request, 'result.html', context)


def get_searchquery(data):
    searchquery = ''
    searchquery += data['people'] if data['people'] else ''
    searchquery += data['gender'] if data['gender'] else ''
    searchquery += data['interested_in'] if data['interested_in'] else ''
    searchquery += data['relationship'] if data['relationship'] else ''
    searchquery += 'str/{}/pages-named/likers/'.format(data['interest']) if data['interest'] else ''
    searchquery += data['location'].format('str/{}/pages-named'.format(data['location_query'])) if data['location_query'] else ''
    searchquery += data['company'].format('str/{}/pages-named'.format(data['company_query'])) if data['company_query'] else ''
    searchquery += data['school'].format('str/{}/pages-named'.format(data['school_query'])) if data['school_query'] else ''
    searchquery += 'str/{}/pages-named/employees/'.format(data['job_title']) if data['job_title'] else ''
    searchquery += 'str/{}/pages-named/speakers/'.format(data['language']) if data['language'] else ''
    searchquery += 'str/{}/pages-named/major/students/present/'.format(data['major']) if data['major'] else ''
    searchquery += get_date(data) if not data['born'] else get_date(data, True)
    searchquery += 'str/{}/users-named'.format(data['name']) if data['name'] else ''
    return searchquery


def get_date(data, range=False):
    date = ''
    if range:
        date += '{}/before/users-born/'.format(data['born_range_to']) if data['born_range_to'] else ''
        date += '{}/after/users-born/'.format(data['born_range_from']) if data['born_range_from'] else ''
    elif data['born_year'] or data['born_month']:
        date = '{}/{}/date-2/users-born/'.format(data['born_year'], data['born_month']) if data['born_month'] else '{}/date/users-born/'.format(data['born_year'])
    return date


def get_html(url):
    sh.loadPage(url)
    return ''


def login(username, password, initial_url='https://www.facebook.com/', login_user_element_path='#email', login_pass_element_path='#pass'):
    sh.loadPage(initial_url)
    sh.selectAndWrite(login_user_element_path, username)
    sh.submitForm(sh.selectAndWrite(login_pass_element_path, password))
