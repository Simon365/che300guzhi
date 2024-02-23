import time
# from appium import webdriver
from selenium import webdriver
from selenium.common import exceptions
# for file operation
import shutil
import os


def peer_sleep(t):
    """
    :param t:
    :return:
    """
    return time.sleep(t)


def peer_get_windows_size(driver):
    """
    :param driver:
    :return:
    """
    try:
        return driver.get_window_size()
    except exceptions.WebDriverException:
        print(" Get the window size failed!")


def peer_swipe(driver, x1, y1, x2, y2, t):
    """
    :param driver:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param t:
    :return:
    """
    try:
        return driver.swipe(x1, y1, x2, y2, t)
    except exceptions.WebDriverException:
        print(" Get the window size failed!")


def peer_snap(driver, filename):
    """
    :param driver:
    :param filename:
    :return:
    """
    try:
        return driver.get_screenshot_as_file(filename)
    except exceptions.WebDriverException:
        print(" Snap the window failed!")


def peer_copy_file():
    while True:
        path = input("请输入要复制的文件的完整路径：")
        if path == "exit":
            return
        path = "r'" + path + "'"
        save_path = input("请输入复制文件保存的详细路径：")
        save_path = "r'" + save_path + "'"
        shutil.copy(path, save_path)


def peer_copy_folder():
    while True:
        path = input("请输入要复制的文件夹的完整路径：")
        if path == "exit":
            return
        path = "r'" + path + "'"
        save_path = input("请输入复制文件夹保存的详细路径：")
        save_path = "r'" + save_path + "'"

        while os.path.exists(save_path):
            print("目标文件夹已经存在，请重新输入！")
            save_path = input("请输入复制文件夹保存的详细路径：")
            if save_path == "exit":
                return
            save_path = "r'" + save_path + "'"

        shutil.copytree(path, save_path)
