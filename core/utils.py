from core import selenium
import json


def login_facebook(username='lizzethcamargo@hotmail.com', password='lasquierobreggethmaria79'):
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


def get_data_search(searchurl, limit=None):
    selenium.init()
    selenium.load_page(searchurl)
    selenium.scrolling_down_facebook(limit)
    ids = selenium.get_elements_class_name('_3u1')
    images = selenium.get_elements_class_name('_1glk')
    names = selenium.get_elements_class_name('_32mo')
    data = []
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


def close_bot():
    selenium.close()
