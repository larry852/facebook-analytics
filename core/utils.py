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


def get_data_search_stories(searchurl, limit=None):
    data = []
    selenium.init()
    selenium.load_page(searchurl)
    try:
        selenium.get_element_id('empty_result_error')
        print('No results --- {} ---'.format(searchurl))
        return data
    except Exception:
        pass
    selenium.scrolling_down_facebook(limit, '_5bl2')
    stories = selenium.get_elements_class_name('_5bl2')
    for storie in stories:
        page_id = json.loads(storie.get_attribute('data-bt'))['owner_id']
        storie_id = json.loads(storie.get_attribute('data-bt'))['id']
        fb_id = str(page_id) + "_" + str(storie_id)
        element = {
            'fb_id': fb_id,
            'url': 'https://www.facebook.com/' + str(fb_id)
        }
        data.append(element)
    return data


def get_data_storie_scrap(fb_id):
    selenium.init()
    selenium.load_page('https://www.facebook.com/' + fb_id)
    entity = selenium.get_element_class_name('_5pb8')
    entity_str = entity.get_attribute('data-hovercard')
    entity_id = entity_str[entity_str.index('?id='):].replace('?id=', '')
    entity_name = selenium.get_child_tag_name(entity, 'img').get_attribute('aria-label')
    message = selenium.get_element_class_name('userContent').text
    open_reactions = selenium.get_element_class_name('_3t53')
    selenium.click(open_reactions)
    div_reactions = selenium.get_element_class_name('_ds-')
    span_reactions = selenium.get_child_tag_name(div_reactions, 'span')
    reactions = selenium.get_childs_tag_name(span_reactions, 'span')
    for reaction in reactions:
        print(reaction.get_attribute('aria-label'))

    try:
        image = selenium.get_element_class_name('fbStoryAttachmentImage')
        image_url = selenium.get_child_tag_name(image, 'img').get_attribute('src')
    except Exception:
        try:
            image = selenium.get_element_class_name('_3x-2')
            image_url = selenium.get_child_tag_name(image, 'img').get_attribute('src')
        except Exception:
            image_url = None

    data = {
        'id': fb_id,
        'from': {'id': entity_id, 'name': entity_name},
        'message': message,
        'picture': image_url,
    }
    return data


def close_bot():
    selenium.close()
