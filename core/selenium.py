from selenium import webdriver

driver = None


def init():
    global driver
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome("/home/larry/.chromedriver", chrome_options=chrome_options) if driver is None else driver


def load_page(page):
    driver.get(page)


def submit_form(element):
    element.submit()


def get_element_id(id):
    return driver.find_element_by_id(id)


def get_element_xpath(xpath):
    return driver.find_element_by_xpath(xpath)


def get_element_class_name(class_name):
    return driver.find_element_by_class_name(class_name)


def get_elements_class_name(class_name):
    return driver.find_elements_by_class_name(class_name)


def set_text_input(input, text):
    input.send_keys(text)


def save_screenshoot(filePath):
    driver.save_screenshot(filePath)


def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scrolling_down_facebook(limit):
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        try:
            if limit and limit <= len(driver.find_elements_by_class_name('_3u1')):
                break
            driver.find_element_by_class_name('_24j')
            break
        except Exception:
            continue


def click(element):
    element.click()


def close():
    global driver
    driver.quit()
    driver = None
