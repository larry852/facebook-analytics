from . import selenium
import json


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
    searchquery += 'str/{}/users-named/'.format(data['name']) if data['name'] else ''
    return searchquery


def get_date(data, range=False):
    date = ''
    if range:
        date += '{}/before/users-born/'.format(data['born_range_to']) if data['born_range_to'] else ''
        date += '{}/after/users-born/'.format(data['born_range_from']) if data['born_range_from'] else ''
    elif data['born_year'] or data['born_month']:
        date = '{}/{}/date-2/users-born/'.format(data['born_year'], data['born_month']) if data['born_month'] else '{}/date/users-born/'.format(data['born_year'])
    return date


def login_facebook(username, password):
    selenium.init()
    initial_url = 'https://www.facebook.com/'
    login_user_element_xpath = '//*[@id="email"]'
    login_pass_element_xpath = '//*[@id="pass"]'
    selenium.load_page(initial_url)
    element_user = selenium.get_element_xpath(login_user_element_xpath)
    element_password = selenium.get_element_xpath(login_pass_element_xpath)
    selenium.set_text_input(element_user, username)
    selenium.set_text_input(element_password, password)
    selenium.submit_form(element_password)


def get_data_profiles_search(searchurl, limit=None):
    selenium.init()
    selenium.load_page(searchurl)
    selenium.scrolling_down_facebook(limit)
    id_profiles = selenium.get_elements_class_name('_3u1')
    image_profiles = selenium.get_elements_class_name('_1glk')
    name_profiles = selenium.get_elements_class_name('_32mo')
    profiles = []
    for index, value in enumerate(id_profiles):
        id = json.loads(value.get_attribute('data-bt'))['id']
        profile = {
            'id': id,
            'name': name_profiles[index].text,
            'image': image_profiles[index].get_attribute('src'),
            'url': 'https://www.facebook.com/' + str(id)
        }
        profiles.append(profile)
    return profiles


def close_bot():
    selenium.close()
