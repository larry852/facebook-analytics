from core import utils as core_utils
from .models import Entity, Relation
from django.shortcuts import redirect


def generate(profiles):
    import time
    start_time = time.time()

    core_utils.login_facebook()
    for profile in profiles:
        searchurl_pages = 'https://www.facebook.com/search/{}/pages-liked'.format(profile.fb_id)
        searchurl_groups = 'https://www.facebook.com/search/{}/groups'.format(profile.fb_id)
        pages = core_utils.get_data_search(searchurl_pages, 10)
        groups = core_utils.get_data_search(searchurl_groups, 10)
        save_pages(pages, profile)
        save_groups(groups, profile)
    # core_utils.close_bot()
    print("Get topics --- {} seconds ---".format(time.time() - start_time))
    return redirect('/admin/topics/entity/')


def save_pages(pages, profile):
    for page in pages:
        entity, created = Entity.objects.get_or_create(fb_id=page['fb_id'], name=page['name'], image=page['image'], type='page')
        entity.save()
        Relation.objects.get_or_create(entity=entity, profile=profile)


def save_groups(groups, profile):
    for group in groups:
        entity, created = Entity.objects.get_or_create(fb_id=group['fb_id'], name=group['name'], image=group['image'], type='group')
        entity.save()
        Relation.objects.get_or_create(entity=entity, profile=profile)
