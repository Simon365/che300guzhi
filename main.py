import unittest
from module import *


class Test_che300_valuation(unittest.TestCase):
    def setUp(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--start-maximized')
        options.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(options=options)
        pause()

    def test_run(self):
        # while True:
        #     # input parameter
        #     index = input("请输入一共有多少条要查询数据。\n 数据条数：")
        #     if index.isdigit():
        #         index = int(index)
        #         line_no = input("请输入开始查询的行号，标题为第0行！\n 开始行号：")
        #         if line_no.isdigit():
        #             line_no = int(line_no)
        #             image_path = input("请输入截图保存地址，确保在根目录下，文件夹名称为应为字母，例如 e:/snap/ \n 截图保存地址：")
        #             break

        # init excel
        file_path = "e:/che300guzhi.xls"
        new_file_path = "e:/new_che300guzhi.xls"
        image_path = "e:/guzhi/"

        # read original file
        workbook = xlrd.open_workbook(file_path)
        worksheet = workbook.sheet_by_name("data")
        head0 = worksheet.cell(0, 0).value
        head1 = worksheet.cell(0, 8).value
        head2 = worksheet.cell(0, 9).value

        # init new excel file
        new_workbook = xlwt.Workbook()
        new_worksheet = new_workbook.add_sheet("data")
        new_worksheet.write(0, 0, head0)
        new_worksheet.write(0, 1, head1)
        new_worksheet.write(0, 2, head2)
        new_workbook.save(new_file_path)
        line_no = 2
        index = 1

        driver = self.driver
        url = "https://www.che300.com/pinggu"
        init_che300(driver, url)
        get_value(driver, new_file_path, new_workbook, new_worksheet, worksheet, image_path, line_no, index)

    def tearDown(self):
        while True:
            flag = input("是否关闭测试窗口？关闭窗口 y， 保留窗口 n。\n 请输入：")
            if flag.lower() == "y":
                break

        s_sleep()
        self.driver.close()


# 创建主程序入口
if __name__ == '__main__':
    unittest.main()
