from core import utils as core_utils
import time


def main(data):
    start_time = time.time()

    searchquery = get_searchquery(data)
    searchurl = 'https://www.facebook.com/search/{}'.format(searchquery)
    core_utils.login_facebook()
    # limit = int(data['limit']) if data['limit'] else None
    # profiles = core_utils.get_data_search_profiles(searchurl, limit)
    # list_querys = get_querys(data)
    # query = save_query(list_querys)
    # save_profiles(profiles, query)
    core_utils.close_bot()
    context = {'searchurl': searchurl, 'stories': 'stories'}

    print("Get stories --- {} seconds ---".format(time.time() - start_time))

    return context


def get_searchquery(data):
    searchquery = ''
    searchquery += 'str/{}/stories-keyword/stories-public'.format(data['query']) if data['query'] else ''
    return searchquery
