from core import utils as core_utils, google
import time
import json
from urllib.request import urlopen
from .models import Query, Entity, Attachment, Storie, Comment, Reaction
from django.utils import timezone


def main(data):
    start_time = time.time()

    stories = []
    searchquery = get_searchquery(data)
    searchurl = 'https://www.facebook.com/search/{}'.format(searchquery)
    core_utils.login_facebook()
    limit = int(data['limit']) if data['limit'] else None
    data_stories = core_utils.get_data_search_stories(searchurl, limit)

    # data_stories = [data_stories[2]]

    total_count_post = len(data_stories)
    print("Total post: " + str(total_count_post))
    print("")
    for index, data_storie in enumerate(data_stories):
        print("Process: " + str(index + 1) + "/" + str(total_count_post))
        data_api = get_data_storie_api(data_storie['fb_id'])
        if data_api:
            stories.append(data_api)
    core_utils.close_bot()
    list_querys = get_querys(data)
    query = save_query(list_querys)
    save_stories(stories, query)
    context = {'searchurl': searchurl, 'stories': stories}

    print("Get stories --- {} seconds ---".format(time.time() - start_time))

    return context


def get_searchquery(data):
    searchquery = ''
    searchquery += 'str/{}/stories-keyword/stories-public?'.format(data['query']) if data['query'] else ''
    searchquery += '&filters_rp_location=%7B"name"%3A"location"%2C"args"%3A"{}"%7D'.format(data['location']) if data['location'] else ''
    searchquery += '&filters_rp_creation_time=%7B"name"%3A"creation_time"%2C"args"%3A"%7B%5C"start_year%5C"%3A%5C"{}%5C"%2C%5C"start_month%5C"%3A%5C"{}-{}%5C"%2C%5C"end_year%5C"%3A%5C"{}%5C"%2C%5C"end_month%5C"%3A%5C"{}-{}%5C"%7D"%7D'.format(data['start_year'], data['start_year'], data['start_month'], data['end_year'], data['end_year'], data['end_month']) if data['start_year'] and data['start_month'] and data['end_year'] and data['end_month'] else ''
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
            if not Storie.objects.filter(fb_id=storie['id']).exists():
                try:
                    entity, created = Entity.objects.get_or_create(fb_id=storie['from']['id'], name=storie['from']['name'])
                except Exception:
                    entity, created = Entity.objects.get_or_create(fb_id=storie['id'], name="Group of Facebook")

                try:
                    storie['description']
                except Exception:
                    storie['description'] = None
                try:
                    storie['message']
                except Exception:
                    storie['message'] = None
                try:
                    storie['name']
                except Exception:
                    storie['name'] = None
                try:
                    if storie['picture'] is None:
                        storie['picture'] = '/media/topics/fb_post.gif'
                except Exception:
                    storie['picture'] = '/media/topics/fb_post.gif'

                attachment, created = Attachment.objects.get_or_create(title=storie['name'], description=storie['description'], message=storie['message'], media=storie['picture'])

                try:
                    storie['shares']['count']
                except Exception:
                    storie['shares'] = {'count': 0}

                try:
                    storie['created_time']
                except Exception:
                    storie['created_time'] = timezone.now()

                storie['sentiment'] = get_sentiment(storie['message'])

                storieDB, created = Storie.objects.get_or_create(fb_id=storie['id'], entity=entity, attachment=attachment, date=storie['created_time'], query=query, shares=storie['shares']['count'], sentiment=storie['sentiment'])

                try:
                    for comment in storie['comments']:
                        comment['sentiment'] = get_sentiment(comment['message'])
                        Comment.objects.get_or_create(fb_id=comment['fb_id'], message=comment['message'], date=comment['date'], storie=storieDB, sentiment=comment['sentiment'])
                except Exception:
                    pass

                try:
                    for reaction in storie['reactions']:
                        Reaction.objects.get_or_create(type=reaction['type'], count=reaction['count'], storie=storieDB)
                except Exception:
                    Reaction.objects.get_or_create(type='NONE', count=0, storie=storieDB)
        except Exception:
            print("--- Error Data Storie ---  ")
            print(storie)
            print("")


def get_data_storie_api(fb_id):
    data = []
    app_id = '1093188044136348'
    app_secret = 'a640322e7fc689fc1a62a92319c281e0'
    access_token = app_id + '|' + app_secret
    base = 'https://graph.facebook.com/v2.11'
    fields = "id,created_time,description,from,message,name,picture,shares"
    url = "{}/{}/?&access_token={}&fields={}".format(base, fb_id, access_token, fields)
    try:
        resp = urlopen(url).read().decode(encoding='utf-8', errors='ignore')
        print("--- Getting data of API ---  ")
        print("")
    except Exception:
        print("--- Getting data of Selenium ---  ")
        print("")
        data = core_utils.get_data_storie_scrap(fb_id)
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


def get_sentiment(text):
    return google.analyze_sentiment(text)
