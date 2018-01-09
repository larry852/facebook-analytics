from core import utils as core_utils
from .models import Page, Like


def generate(pages):
    core_utils.login_facebook()
    for page in pages:
        searchurl = 'https://www.facebook.com/search/{}/pages-liked'.format(page.fb_id)
        pages = core_utils.get_data_search(searchurl, 20)
        save_pages(pages, page)
    core_utils.close_bot()


def save_pages(pages, profile):
    for page in pages:
        page_model = Page(fb_id=page['fb_id'], name=pages['name'], image=pages['image'])
        page_model.save()
        Like(page=page_model, profile=profile)
