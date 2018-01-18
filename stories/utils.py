from core import utils as core_utils
import time
import json
from urllib.request import urlopen


def main(data):
    start_time = time.time()

    # searchquery = get_searchquery(data)
    # searchurl = 'https://www.facebook.com/search/{}'.format(searchquery)
    # core_utils.login_facebook()
    # limit = int(data['limit']) if data['limit'] else None
    # stories = core_utils.get_data_search_stories(searchurl, limit)

    print(get_data_storie_api('114138019012560_309252112834482'))

    # list_querys = get_querys(data)
    # query = save_query(list_querys)
    # save_profiles(profiles, query)

    # core_utils.close_bot()
    context = {'searchurl': 'searchurl', 'stories': 'stories'}

    print("Get stories --- {} seconds ---".format(time.time() - start_time))

    return context


def get_searchquery(data):
    searchquery = ''
    searchquery += 'str/{}/stories-keyword/stories-public'.format(data['query']) if data['query'] else ''
    searchquery += '?filters_rp_location=%7B"name"%3A"location"%2C"args"%3A"{}"%7D'.format(data['location']) if data['location'] else ''
    return searchquery


def get_data_storie_api(fb_id):
    app_id = '1093188044136348'
    app_secret = 'a640322e7fc689fc1a62a92319c281e0'
    access_token = app_id + '|' + app_secret
    base = 'https://graph.facebook.com/v2.11'
    fields = "id,created_time,description,from,icon,link,message,name,object_id,picture,place,shares,source,story,to,with_tags"
    url = "{}/{}/?&access_token={}&fields={}".format(base, fb_id, access_token, fields)
    print(url)
    resp = urlopen(url).read().decode(encoding='utf-8', errors='ignore')
    data = json.loads(resp)

    type_reactions = {'NONE', 'LIKE', 'LOVE', 'WOW', 'HAHA', 'SAD', 'ANGRY', 'THANKFUL'}
    reactions = []
    for type_reaction in type_reactions:
        url = "{}/{}/reactions/?&access_token={}&summary=total_count&type={}".format(base, fb_id, access_token, type_reaction)
        resp = urlopen(url).read().decode(encoding='utf-8', errors='ignore')
        reaction = {'type': type_reaction, 'count': json.loads(resp)['summary']['total_count']}
        reactions.append(reaction)
    data['reactions'] = reactions

    comments = []
    url = "{}/{}/comments/?&access_token={}&summary=true".format(base, fb_id, access_token)
    resp = urlopen(url).read().decode(encoding='utf-8', errors='ignore')
    for comment in json.loads(resp)['data']:
        comments.append({'date': comment['created_time'], 'fb_id': comment['id'], 'message': comment['message']})
    try:
        while json.loads(resp)["paging"]["next"]:
            url = json.loads(resp)["paging"]["next"]
            resp = urlopen(url).read().decode(encoding='utf-8', errors='ignore')
            for comment in json.loads(resp)['data']:
                comments.append({'date': comment['created_time'], 'fb_id': comment['id'], 'message': comment['message']})
    except Exception:
        pass
    data['comments'] = comments
    return data
