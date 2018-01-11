from core import utils as core_utils
from .models import Entity, Relation
from django.shortcuts import redirect
import time


def main(profiles):
    start_time = time.time()

    core_utils.login_facebook()
    for profile in profiles:
        topics = core_utils.get_data_topics_profile(profile)
        save_topics(topics, profile)
    core_utils.close_bot()

    print("Get topics --- {} seconds ---".format(time.time() - start_time))
    return redirect('/admin/topics/entity/')


def save_topics(topics, profile):
    for topic in topics:
        entity, created = Entity.objects.get_or_create(fb_id=topic['fb_id'], name=topic['name'], image=topic['image'], type=topic['type'])
        entity.save()
        Relation.objects.get_or_create(entity=entity, profile=profile)
