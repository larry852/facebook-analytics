from core import utils as core_utils
import time
import json
from urllib.request import urlopen
from .models import Query, Entity, Attachment, Storie, Comment, Reaction


def main(data):
    start_time = time.time()

    searchquery = get_searchquery(data)
    searchurl = 'https://www.facebook.com/search/{}'.format(searchquery)
    core_utils.login_facebook()
    limit = int(data['limit']) if data['limit'] else None
    data_stories = core_utils.get_data_search_stories(searchurl, limit)
    core_utils.close_bot()
    stories = []
    for data_storie in data_stories:
        stories.append(get_data_storie_api(data_storie['fb_id']))
    list_querys = get_querys(data)
    query = save_query(list_querys)
    save_stories(stories, query)
    context = {'searchurl': searchurl, 'stories': stories}

    print("Get stories --- {} seconds ---".format(time.time() - start_time))

    return context


def get_searchquery(data):
    searchquery = ''
    searchquery += 'str/{}/stories-keyword/stories-public'.format(data['query']) if data['query'] else ''
    searchquery += '?filters_rp_location=%7B"name"%3A"location"%2C"args"%3A"{}"%7D'.format(data['location']) if data['location'] else ''
    return searchquery


def get_querys(data):
    searchquery = ''
    searchquery += '{}/'.format(data['query']) if data['query'] else ''
    searchquery += '{}/'.format(data['location']) if data['location'] else ''
    searchquery += '{}/'.format(data['start_year']) if data['start_year'] else ''
    searchquery += '{}/'.format(data['start_month']) if data['start_month'] else ''
    searchquery += '{}/'.format(data['end_year']) if data['end_year'] else ''
    searchquery += '{}/'.format(data['end_month']) if data['end_month'] else ''
    return searchquery


def save_query(url):
    query = Query(url=url)
    query.save()
    return query


def save_stories(stories, query):
    for storie in stories:
        try:
            entity, created = Entity.objects.get_or_create(fb_id=storie['from']['id'], name=storie['from']['name'])
            entity.save()
        except Exception:
            break

        try:
            description = storie['description']
        except Exception:
            description = None
        try:
            message = storie['message']
        except Exception:
            message = None
        try:
            name = storie['name']
        except Exception:
            name = None
        attachment, created = Attachment.objects.get_or_create(title=name, description=description, message=message, media=storie['picture'])
        attachment.save()

        try:
            pass
        except Exception as e:
            raise e
        storieDB, created = Storie.objects.get_or_create(fb_id=storie['id'], entity=entity, attachment=attachment, date=storie['created_time'], query=query, shares=storie['shares']['count'])
        entity.save()

        for comment in storie['comments']:
            Comment.objects.get_or_create(fb_id=comment['fb_id'], message=comment['message'], date=comment['date'], storie=storieDB)

        for reaction in storie['reactions']:
            Reaction.objects.get_or_create(type=reaction['type'], count=reaction['count'], storie=storieDB)


def get_data_storie_api(fb_id):
    data = []
    app_id = '1093188044136348'
    app_secret = 'a640322e7fc689fc1a62a92319c281e0'
    access_token = app_id + '|' + app_secret
    base = 'https://graph.facebook.com/v2.11'
    fields = "id,created_time,description,from,icon,link,message,name,object_id,picture,place,shares,source,story,to,with_tags"
    url = "{}/{}/?&access_token={}&fields={}".format(base, fb_id, access_token, fields)
    print(url)
    try:
        resp = urlopen(url).read().decode(encoding='utf-8', errors='ignore')
    except Exception:
        return data
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
    # try:
    #     while json.loads(resp)["paging"]["next"]:
    #         url = json.loads(resp)["paging"]["next"]
    #         resp = urlopen(url).read().decode(encoding='utf-8', errors='ignore')
    #         for comment in json.loads(resp)['data']:
    #             comments.append({'date': comment['created_time'], 'fb_id': comment['id'], 'message': comment['message']})
    # except Exception:
    #     pass
    data['comments'] = comments
    return data
