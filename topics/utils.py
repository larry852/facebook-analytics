from core import utils as core_utils


def generate(profiles):
    core_utils.login_facebook()
    for profile in profiles:
        searchurl = 'https://www.facebook.com/search/{}/pages-liked'.format(profile.fb_id)
        topics = core_utils.get_data_query(searchurl, 20)
        print(topics)
        # save_topics(topics, profile)
    core_utils.close_bot()


def save_topics(topics, profile):
    for topic in topics:
        pass
