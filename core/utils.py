from core import selenium
import json


def login_facebook(username='anjare97@hotmail.com', password='08jun1997ggg'):
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


def get_data_search_profiles(searchurl, limit=None):
    data = []
    selenium.init()
    selenium.load_page(searchurl)
    try:
        selenium.get_element_id('empty_result_error')
        print('No results --- {} ---'.format(searchurl))
        return data
    except Exception:
        pass
    selenium.scrolling_down_facebook(limit, '_3u1')
    ids = selenium.get_elements_class_name('_3u1')
    images = selenium.get_elements_class_name('_1glk')
    names = selenium.get_elements_class_name('_32mo')
    for index, value in enumerate(ids):
        fb_id = json.loads(value.get_attribute('data-bt'))['id']
        element = {
            'fb_id': fb_id,
            'name': names[index].text,
            'image': images[index].get_attribute('src'),
            'url': 'https://www.facebook.com/' + str(fb_id)
        }
        data.append(element)
    return data


def get_data_topics_profile(profile, limit=None):
    selenium.init()
    selenium.load_page('https://www.facebook.com/{}'.format(profile.fb_id))
    profile_url = selenium.get_current_url()
    profile_url += '/' if 'profile.php?' not in profile_url else '&sk='
    groups = get_topics_groups(limit, profile_url)
    pages = get_topics_pages(limit, profile_url)
    return groups + pages


def get_topics_groups(limit, profile_url):
    data = []
    selenium.load_page(profile_url + 'groups')
    try:
        selenium.get_elements_class_name('fbTimelineCapsule')
        return data
    except Exception:
        pass
    selenium.scrolling_down_facebook(limit, '_153f')
    groups = []
    possible_groups = selenium.get_elements_class_name('mbs')
    for possible_group in possible_groups:
        if possible_group.get_attribute('innerHTML').startswith('<a href='):
            groups.append(possible_group)
    for group in groups:
        fb_id_html = selenium.get_child_tag_name(group, 'a').get_attribute('data-hovercard')
        fb_id = fb_id_html[fb_id_html.find('?id='):].replace('?id=', '')
        element = {
            'fb_id': fb_id,
            'name': group.text,
            'image': '/media/topics/group_facebook_default.png',
            'url': 'https://www.facebook.com/' + str(fb_id),
            'type': 'group'
        }
        data.append(element)
    return data


def get_topics_pages(limit, profile_url):
    data = []
    selenium.load_page(profile_url + 'likes')
    try:
        selenium.get_element_class_name('fbTimelineCapsule')
        return data
    except Exception:
        pass
    selenium.scrolling_down_facebook(limit, '_5rz')
    pages = []
    possible_pages = selenium.get_elements_class_name('fsl')
    for possible_page in possible_pages:
        if possible_page.get_attribute('innerHTML').startswith('<a href='):
            pages.append(possible_page)
    images = selenium.get_elements_class_name('_8o')
    for index, page in enumerate(pages):
        fb_id_html = selenium.get_child_tag_name(page, 'a').get_attribute('data-hovercard')
        fb_id = fb_id_html[fb_id_html.find('?id='):].replace('?id=', '')
        element = {
            'fb_id': fb_id,
            'name': page.text,
            'image': selenium.get_child_tag_name(images[index], 'img').get_attribute('src'),
            'url': 'https://www.facebook.com/' + str(fb_id),
            'type': 'page'
        }
        data.append(element)
    return data


def close_bot():
    selenium.close()
