from sbase import *


def open_che300_valuation(driver, url):
    try:
        driver.get(url)
        driver.maximize_window()
        s_sleep()
    except exceptions.WebDriverException as e:
        print(format(e))
        return


def login_che300(driver):
    login = find_element_by_class_text(driver, "pc_login", "登录")
    if exist(login):
        login.click()
        s_sleep()
        in_phone = find_element_by_class_placeholder(driver, "form-input", "请输入手机号")
        if not exist(in_phone):
            return False
        in_phone.clear()
        while True:
            flag = input("请输入是否登录成功？登录成功输入y，登录失败输入n!\n 请输入登录状态：")
            if flag.lower() == "y":
                break
        return True

    else:
        print("没有找到登录入口！")
        return False


# select vehicle model
def select_vehicle_model(driver, vehicle_brand, vehicle_year, vehicle_series, vehicle_model):
    obj_type = find_element_by_id(driver, "valnone")
    if obj_type is None:
        return False
    obj_type.click()
    pause()
    pinpai_list = find_element_by_class(driver, "brand")
    pinpai = find_element_by_class_text(driver, "list_1", vehicle_brand)
    if pinpai is None:
        return False
    # dict1 = pinpai.location_once_scrolled_into_view       # direct scroll to element
    scroll_to_element_drop_click(driver, pinpai_list, pinpai)
    pause()
    pinpai.click()
    pause()
    obj_series = find_element_by_class_part_text(driver, "list_2", vehicle_series)
    if obj_series is None:
        print("没有找到车系！估值失败！")
        return False
    else:
        series_list = find_element_by_class(driver, "series")
        if series_list is None:
            print("没有找到车系！估值失败！")
            return False
        scroll_to_element_drop_click(driver, series_list, obj_series)
        s_sleep()
        name_list = find_element_by_class(driver, "simple")
        if name_list is None:
            print("没有找到车型！估值失败！")
            return False
        vehicle_name = vehicle_year + " " + vehicle_series + " " + vehicle_model
        print(vehicle_name)
        vehicle = find_element_by_class_part_text(driver, "model_name", vehicle_name)
        if exist(vehicle):
            scroll_to_element_drop_click(driver, name_list, vehicle)
            s_sleep()
            return True
        return False


# select vehicle year
def select_vehicle_year(driver, vehicle_year, vehicle_month):
    obj_year = find_element_by_id(driver, "select4")
    if obj_year is None:
        print("选择车辆年份失败！")
        return False

    obj_year.click()
    pause()
    vehicle_year = str(vehicle_year)[0:4]
    # print(vehicle_year)
    obj_y = find_element_by_class_part_text(driver, "list_4", vehicle_year)
    if obj_y is None:
        print("选择车辆年份失败！")
        return False
    obj_y.click()
    pause()
    # vehicle_month = str(vehicle_month[0:2])
    # print(vehicle_month)
    obj_month = find_element_by_class_part_text(driver, "list_5", vehicle_month)
    if obj_month is None:
        print("选择车辆月份失败！")
        return False
    obj_month.click()
    pause()
    return True


# select vehicle area
def select_vehicle_area(driver, province, city):
    province_list = ["北京", "天津", "上海", "重庆"]
    obj_area = find_element_by_id(driver, "select5")
    if exist(obj_area) is None:
        print("没有找到城市选择！")
        return False
    pause()
    obj_area.click()
    pause()
    province = str(province)[0:2]
    if province_list.count(province) > 0:
        # 处理直辖市的情况
        obj_province = find_element_by_class_part_text(driver, "list_6", province)
        if exist(obj_province):
            obj_province.click()
            pause()
            return True
        else:
            print("没有找到直辖市！")
            return False
    else:
        city = str(city)[0:2]
        obj_province = find_element_by_class_part_text(driver, "list_6", province)
        province_list = find_element_by_class(driver, "select_province")
        if exist(obj_province):
            scroll_to_element_drop_click(driver, province_list, obj_province)
            pause()
            city_list = find_element_by_class(driver, "select_city")
            obj_city = find_element_by_class_part_text(driver, "list_7", city)
            if exist(obj_city):
                scroll_to_element_drop_click(driver, city_list, obj_city)
                s_sleep()
                return True
        print("没有找到城市！")
        return False


# enter the li cheng
def enter_li_cheng(driver, licheng):
    obj_licheng = find_element_by_id(driver, "lichengpd")
    if exist(obj_licheng):
        obj_licheng.clear()
        pause()
        print(licheng)
        obj_licheng.send_keys(int(licheng))
        s_sleep()
        return True
    else:
        print("输入里程失败！")
        return False


# confirm and valuation
def confirm_valuation(driver):
    confirm = find_element_by_id(driver, "eval")
    if exist(confirm):
        confirm.click()
        s_sleep()
    else:
        print("估值失败，请人工处理！")
        return False


# record the valuation, return the lower and higher valuation
def record_valuation(driver, image_path):
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    s_sleep()
    status = ""
    low_value = ""
    high_value = ""
    # chuli shuju
    # obj_status = find_element_by_class_part_text(driver, "on", "车况")
    # if exist(obj_status):
    #     status = obj_status.text
    # else:
    #     print("保存估值失败，请人工处理！")
    # obj_low =

    # snap
    snap(driver, image_path)
    driver.close()
    driver.switch_to.window(handles[0])
    return




