from spec import *


def init_che300(driver, url):
    open_che300_valuation(driver, url)
    # if login_che300(driver):
    #     print("登录成功！")


def get_value(driver, new_file, new_wb, new_ws, ws, image_path, line_no, index):
    i = 0
    for i in range(0, index):
        print("current line no is : %s" % line_no)
        vin = ws.cell(line_no, 0).value
        brand = ws.cell(line_no, 3).value
        year = ws.cell(line_no, 4).value
        series = ws.cell(line_no, 5).value
        model = ws.cell(line_no, 6).value
        province = ws.cell(line_no, 7).value
        city = ws.cell(line_no, 8).value
        f_year = ws.cell(line_no, 9).value
        f_month = ws.cell(line_no, 10).value
        licheng = ws.cell(line_no, 11).value

        if not select_vehicle_model(driver, brand, year, series, model):
            print("查找车型失败！")
            line_no = line_no + 1
            continue
        if not select_vehicle_year(driver, f_year, f_month):
            print("选择上牌年月失败！")
            line_no = line_no + 1
            continue
        if not select_vehicle_area(driver, province, city):
            print("选择地区失败！")
            line_no = line_no + 1
            continue
        if not enter_li_cheng(driver, licheng):
            print("输入里程失败！")
            line_no = line_no + 1
            continue
        # if not confirm_valuation(driver):
        #     line_no = line_no + 1
        #     continue
        # i_path = image_path + vin + ".png"
        # record_valuation(driver, i_path)
        # line_no = line_no + 1

