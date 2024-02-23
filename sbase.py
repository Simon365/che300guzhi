import time
from typing import List
import win32gui
import win32con
import string
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from base import *
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def scroll_to_top(driver):
    if driver is not None:
        if driver.name == 'chrome':
            js = 'var q = document.body.scrollTop = 0'
        else:
            js = 'var q = document.documentElement.scrollTop = 0'

        try:
            return driver.execute_script(js)
        except exceptions.JavascriptException as e:
            print(format(e))
            return False


# scroll to page bottom
def scroll_to_bottom(driver):
    if driver is not None:
        size = peer.peer_get_windows_size(driver)
        if driver.name == 'chrome':
            js = 'var q = document.body.scrollTop = ' + str(size['height'])
        else:
            js = 'var q = document.documentElement.scrollTop = ' + str(size['height'])

        try:
            return driver.execute_script(js)
        except exceptions.JavascriptException as e:
            print(format(e))
            return False


# scroll to page right
def scroll_to_page_right(driver, x):
    """
    :param driver:
    :param x:
    :return:
    """
    if driver is not None:
        size = peer.peer_get_windows_size(driver)
        y = size['height'] / 2
        js = 'window.scrollTo(-' + str(x) + ', ' + str(y) + ')'
        try:
            return driver.execute_script(js)
        except exceptions.JavascriptException as e:
            print(format(e))
            return False


# scroll to page left
def scroll_to_page_left(driver, x=0):
    """
    :param driver:
    :param x:
    :return:
    """
    if driver is not None:
        return scroll_to_page_right(driver, x)


# scroll to page top
def scroll_to_page_top(driver):
    if driver is not None:
        js = 'window.scrollTo(0, 0)'
        try:
            return driver.execute_script(js)
        except exceptions.JavascriptException as e:
            print(format(e))
            return False


# scroll to window bottom
def scroll_to_page_bottom(driver):
    if driver is not None:
        js = 'window.scrollTo(0, document.body.scrollHeight)'
        try:
            return driver.execute_script(js)
        except exceptions.JavascriptException as e:
            print(format(e))
            return False


# 通过id查找元素
def find_element_by_id(driver, rid) -> WebElement:
    """
    :param driver:
    :param rid:
    :return:
    """
    if driver is not None:
        try:
            ele = driver.find_element(By.ID, rid)
            return ele
        except exceptions.NoSuchElementException as e:
            print(format(e))
            print("can not find the %s element !" % rid)
            return None


# 通过tag标签和标签内的文本查找元素
def find_element_by_tag_text(driver, tag, text) -> WebElement:
    """
    :param driver:
    :param tag:
    :param text:
    :return:
    """
    if driver is not None:
        try:
            els = driver.find_elements(By.TAG_NAME, tag)
            m_sleep()
            for element in els:
                if text == element.text:
                    return element
        except exceptions.JavascriptException as e:
            print(format(e))
            print("can not find the %s element !!!" % tag)


# 通过class和标签内的文本查找元素
def find_element_by_class_text(driver, classname, text) -> WebElement:
    """
    :param driver:
    :param classname:
    :param text:
    :return:
    """
    if driver is not None:
        try:
            if text == "":
                ele = driver.find_element(By.CLASS_NAME, classname)
                return ele
            else:
                els = driver.find_elements(By.CLASS_NAME, classname)
                for element in els:
                    if text == element.text:
                        return element
        except exceptions.JavascriptException as e:
            print(format(e))
            print("can not find the %s element !" % classname)
            return None


# 通过class和标签内的部分文本查找元素
def find_element_by_class_part_text(driver, classname, text) -> WebElement:
    """
    :param driver:
    :param classname:
    :param text:
    :return:
    """
    if driver is not None:
        try:
            if text == "":
                ele = driver.find_element(By.CLASS_NAME, classname)
                return ele
            else:
                els = driver.find_elements(By.CLASS_NAME, classname)
                for element in els:
                    if is_substring(element.text, text):
                        return element
        except exceptions.JavascriptException as e:
            print(format(e))
            print("can not find the %s element !" % classname)
            return None


# 通过class和标签内的部分文本查找元素
def find_element_by_class_multi_part_text(driver, classname, text1, text2,  text3) -> WebElement:
    """
    :param driver:
    :param classname:
    :param text1:
    :param text2:
    :param text3:
    :return:
    """
    if driver is not None:
        try:
            if text1 == "":
                ele = driver.find_element(By.CLASS_NAME, classname)
                return ele
            else:
                elist1 = []
                els = driver.find_elements(By.CLASS_NAME, classname)
                for el1 in els:
                    if is_substring(el1.text, text1):
                        elist1.append(el1)
                if len(elist1) > 0:
                    elist2 = []
                    for el2 in elist1:
                        if is_substring(el2.text, text2):
                            elist2.append(el2)
                    if len(elist2) > 0:
                        for ele in elist2:
                            if is_substring(ele.text, text3):
                                return ele
                return None
        except exceptions.JavascriptException as e:
            print(format(e))
            print("can not find the %s element !" % classname)
            return None


# 通过class查找元素
def find_element_by_class(driver, class_name) -> WebElement:
    """
    :param driver:
    :param class_name:
    :return:
    """
    if driver is not None:
        try:
            ele = driver.find_element(By.CLASS_NAME, class_name)
            return ele
        except exceptions.NoSuchElementException as e:
            print(format(e))
            print("can not find the %s element !" % class_name)


# 通过xpath查找元素
def find_element_by_xpath(driver, path) -> WebElement:
    if driver is not None:
        try:
            return driver.find_element(By.XPATH, path)
        except exceptions.NoSuchElementException as e:
            print(format(e))
            print("can't find the %s element!" % path)


# 通过xpath查找元素列表
def find_elements_by_xpath(driver, path) -> List:
    if driver is not None:
        try:
            return driver.find_elements(By.XPATH, path)
        except exceptions.NoSuchElementException as e:
            print(format(e))
            print("can't find the %s element!" % path)


# 获取占位符提示文字
def get_placeholder(driver, element) -> string:
    """
    :param driver:
    :param element:
    :return:
    """
    return driver.execute_script('return arguments[0].placeholder;', element)


# 通过tag和placeholder查找指定的元素
def find_element_by_tag_placeholder(driver, tag, placeholder) -> WebElement:
    """
    :param driver:
    :param tag:
    :param placeholder:
    :return:
    """
    if driver is not None:
        try:
            els = driver.find_elements(By.TAG_NAME, tag)
            pause()
            for element in els:
                if placeholder == get_placeholder(driver, element):
                    return element
        except exceptions.NoSuchElementException as e:
            print(format(e))
            print("can't find the %s element!" % tag)


# 通过tag和placeholder查找指定的元素
def find_element_by_class_placeholder(driver, class_name, placeholder) -> WebElement:
    """
    :param driver:
    :param class_name:
    :param placeholder:
    :return:
    """
    if driver is not None:
        try:
            els = driver.find_elements(By.CLASS_NAME, class_name)
            pause()
            for element in els:
                if placeholder == get_placeholder(driver, element):
                    return element
        except exceptions.NoSuchElementException as e:
            print(format(e))
            print("can't find the %s element!" % class_name)


# find elements by tag name
def find_elements_by_tag_name(driver, tag) -> List:
    if driver is not None:
        try:
            eles = driver.find_elements(By.TAG_NAME, tag)
            return eles
        except exceptions.NoSuchElementException as e:
            print(format(e))
            print("can't find the %s elements!" % tag)


# find single element by tag name
def find_element_by_tag_name(driver, tag) -> WebElement:
    if driver is not None:
        try:
            ele = driver.find_element(By.TAG_NAME, tag)
            return ele
        except exceptions.NoSuchElementException as e:
            print(format(e))
            print("can't find the %s element!" % tag)


# scroll to the specific element
def scroll_to_element(driver, element):
    """
    :param driver:
    :param element:
    :return:
    """
    if driver is not None:
        try:
            driver.execute_script('arguments[0].scrollIntoView();', element)
        except exceptions.JavascriptException as e:
            print(format(e))
            print("page scroll failed!")


# page scroll to element and click
def scroll_to_element_click(driver, element):
    """
        :param driver:
        :param element:
        :return:
        """
    if driver is not None:
        try:
            driver.execute_script('arguments[0].scrollIntoView();', element)
            s_sleep()
            element.click()
            pause()
        except exceptions.JavascriptException as e:
            print(format(e))
            print("page scroll failed!")


# drop scroll to element and click, multi paras just list them!!!
def scroll_to_element_drop_click(driver, drop, element):
    """
        :param driver:
        :param drop:
        :param element:
        :return:
        """
    if driver is not None:
        try:
            driver.execute_script('arguments[0].scrollTo(0, arguments[1].offsetTop)', drop, element)
            s_sleep()
            element.click()
            pause()
        except exceptions.JavascriptException as e:
            print(format(e))
            print("page scroll failed!")


# upload_file: use os control and method upload a file to the webserver.
# filepath file path witch to be uploaded;
# browser_Type browser type such as Chrome, Firefox etc.
def upload_file(filepath, browser_type):
    # Chrome
    if browser_type == "Chrome":
        title = "打开"
        print("尝试找上传文件对话框！")
        time.sleep(1)
    else:  # Firefox
        title = "文件上传"
        pause()

    # top level window 'open window'
    dialog = win32gui.FindWindow("#32770", title)
    pause()
    # second level
    comboboxex32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)
    pause()
    # Third level
    combobox = win32gui.FindWindowEx(comboboxex32, 0, "ComboBox", None)
    pause()
    # Fourth level, find the file path edit box and upload button.
    edit = win32gui.FindWindowEx(combobox, 0, "Edit", None)
    pause()
    button = win32gui.FindWindowEx(dialog, 0, "Button", None)
    pause()

    # input the filepath to the edit box which input the file path.
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filepath)
    pause()
    # click the button to upload.
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
    pause()


# 通过爱企查获得车商电话号码
def aiqicha_get_phone_no(driver, name) -> str:
    # 首先清空搜索框内容
    driver.get('https://aiqicha.baidu.com/company_detail_11277423681652')
    pause()
    driver.maximize_window()
    m_sleep()
    phone = ''
    try:
        # close = find_element_by_xpath(driver, '/html/body/div[1]/div[1]/header/div/div[2]/img')
        # close.click()
        # pause()
        # 清空企业名称输入字段
        name_input = find_element_by_xpath(driver, '//*[@id="aqc-header-search-input"]')
        name_input.clear()
        pause()
        # 输入企业名称
        name_input.send_keys(name)
        pause()
        # 搜索企业信息
        search = find_element_by_xpath(driver, '/html/body/div[1]/div[1]/header/div/div[2]/button')
        search.click()
        s_sleep()
        # 获得企业的电话
        phone = find_element_by_xpath(driver, '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[5]/'
                                              'div[1]/div[1]/div/span[2]/span/span').text
    except exceptions.ElementNotInteractableException as e:
        print(format(e))

    return phone
