import peer
import re
from functools import wraps
from random import *
import pymysql
# mysql数据库引擎
from sqlalchemy import create_engine
import xlwt
import xlrd
from pandas import DataFrame
from pandas import Series

# for email
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart


def sleep(t):
    peer.peer_sleep(t)


def pause():
    peer.peer_sleep(0.1)


def s_sleep():
    peer.peer_sleep(0.5)


def m_sleep():
    peer.peer_sleep(3)


def l_sleep():
    peer.peer_sleep(10)


def wait():
    peer.peer_sleep(15)


def swipe_up(driver, t=500, n=1):
    """
    :param driver:
    :param t:
    :param n:
    :return:
    """
    if driver is not None:
        # get screen size
        size = peer.peer_get_windows_size(driver)
        w = size['width']  # get the screen width
        h = size['height']  # get the screen height
        s_sleep()
        x1 = w / 2
        y1 = 3 * h / 4
        y2 = h / 4
        for i in range(n):
            peer.peer_swipe(driver, x1, y1, x1, y2, t)


def swipe_down(driver, t=500, n=1):
    """
    :param driver:
    :param t:
    :param n:
    :return:
    """
    if driver is not None:
        # get screen size
        size = peer.peer_get_windows_size(driver)
        w = size['width']  # get the screen width
        h = size['height']  # get the screen height
        s_sleep()
        x1 = w / 2
        y2 = 3 * h / 4
        y1 = h / 4
        for i in range(n):
            peer.peer_swipe(driver, x1, y1, x1, y2, t)


def swipe_left(driver, t=500, n=1):
    """
    :param driver:
    :param t:
    :param n:
    :return:
    """
    if driver is not None:
        # get screen size
        size = peer.peer_get_windows_size(driver)
        w = size['width']  # get the screen width
        h = size['height']  # get the screen height
        s_sleep()
        y1 = h / 4
        x1 = 3 * w / 4
        x2 = w / 4
        for i in range(n):
            peer.peer_swipe(driver, x1, y1, x2, y1, t)


def swipe_right(driver, t=500, n=1):
    """
    :param driver:
    :param t:
    :param n:
    :return:
    """
    if driver is not None:
        # get screen size
        size = peer.peer_get_windows_size(driver)
        w = size['width']  # get the screen width
        h = size['height']  # get the screen height
        s_sleep()
        y1 = h / 4
        x2 = 3 * w / 4
        x1 = w / 4
        for i in range(n):
            peer.peer_swipe(driver, x1, y1, x2, y1, t)


def exist(element):
    """
    :param element:
    :return:
    """
    flag = True
    if element is not None:
        try:
            element.location
        except peer.e as e:
            print(format(e))
            flag = False
    else:
        flag = False

    return flag


def snap(driver, filename):
    # get the screen snap
    if driver is not None:
        return peer.peer_snap(driver, filename)


# snap and record successful test result
def snap_record_succ(driver, image_path, ws_test, line_no, desc) -> int:
    """
    :param driver:
    :param image_path:
    :param ws_test:
    :param line_no:
    :param desc:
    :return:
    """
    if driver is not None:
        try:
            image = image_path + str(line_no).zfill(4) + desc + '.png'
            peer.peer_snap(driver, image)
            ws_test.write(line_no, 0, desc)  # record the test case name
            ws_test.write(line_no, 1, 'pass')  # record the test result
            ws_test.write(line_no, 2, 'file:\\\\' + image)  # record the snap link
            pause()

        except peer.e as e:
            print(format(e))

        return line_no + 1


# snap and record successful test result
def snap_record_fail(driver, image_path, ws_test, line_no, desc) -> int:
    """
    :param driver:
    :param image_path:
    :param ws_test:
    :param line_no:
    :param desc:
    :return:
    """
    if driver is not None:
        try:
            image = image_path + str(line_no).zfill(4) + desc + '.png'
            peer.peer_snap(driver, image)
            ws_test.write(line_no, 0, desc)  # record the test case name
            ws_test.write(line_no, 1, 'fail')  # record the test result
            ws_test.write(line_no, 2, 'file:\\\\' + image)  # record the snap link
            pause()
        except peer.e as e:
            print(format(e))

        return line_no + 1


# pwd = "thzknfbgahxwcagg"
pwd = "biomntfogpdabggf"


# the followed for decorator
def decorator_sample1(func):
    print("do something before executing func")
    print(func())


def decorator_sample2(func):
    def wrapthefunc():
        print("do sth before the func......")
        func()
        print("do sth after the func......")

    return wrapthefunc


@decorator_sample2
def func_requiring_decoration():
    print("I am the func which needs some decoration to do sth.")


def decorator_sample3(func):
    @wraps(func)
    def new_wrap_the_func():
        print("do sth before the func......")
        func()
        print("do sth after the func......")

    return new_wrap_the_func


@decorator_sample3
def newfunc_requiring_decoration():
    print("I am the func which needs some decoration to do sth.")


def use_logging(func):
    @wraps(func)
    def _deco(*args, **kwargs):
        print("%s is running......" % func.__name__)
        func(*args, **kwargs)

    return _deco


# decorator with para
def use_logging_with_para(flag):
    def _deco(func):
        def __deco(*args, **kwargs):
            if flag == "warn":
                print("%s is running" % func.__name__)
            return func(*args, **kwargs)

        return __deco

    return _deco


@use_logging_with_para("warn")
def _bar(a, b):
    print(" I am bar: %s" % (a + b))


@use_logging
def bar(a, b):
    print(" I am bar: %s" % (a + b))


@use_logging
def foo(a, b, c):
    print("I am bar: %s" % (a + b + c))


# adaptive the decorator with para or without para
def decorator_adaptive_para(arg):
    if callable(arg):
        # 判断传入的参数是否是函数，不带参数的装饰器调用这个分支
        @wraps(arg)
        def _deco(*args, **kwargs):
            print("%s is running" % arg.__name__)
            arg(*args, **kwargs)

        return _deco
    else:
        # 带参数的装饰器调用这个分支
        def _deco(func):
            @wraps(func)
            def __deco(*args, **kwargs):
                if arg == "warn":
                    print("warn %s is running" % func.__name__)
                return func(*args, **kwargs)

            return __deco

        return _deco


@decorator_adaptive_para("warn")
# @decorator_adaptive_para
def bar():
    print("I am bar")
    print(bar.__name__)


class Logging(object):
    def __init__(self, level="warn"):
        self.level = level

    def __call__(self, func):
        @wraps(func)
        def _deco(*args, **kwargs):
            if self.level == "warn":
                print('Now %s running the super class!' % func.__name__)
                self.notify(func)
            return func(*args, **kwargs)

        return _deco

    def notify(self, func):
        # implement of notify
        print("%s is running" % func.__name__)


@Logging(level="warn")
def bar(a, b):
    print("I am bar: %s" % (a + b))


class EmailLogging(Logging):
    """
    一个类 logging的实现版本，在函数调用时发送email给管理员
    """

    def __init__(self, email="admin@myproject.com", *args, **kwargs):
        self.email = email
        super(EmailLogging, self).__init__(*args, **kwargs)

    def notify(self, func):
        # email to self.email
        print("%s is running__" % func.__name__)
        print("__sending email to %s" % self.email)


@EmailLogging(level="warn")
def bar1(a, b):
    print("I am bar: %s" % (a + b))


# 对类进行装饰的装饰器
def log_getattribute(cls):
    # get the original implementation
    orig_getattribute = cls.__getattribute__

    # make a new definition
    def new_getattribute(self, name):
        print("getting:", name)
        return orig_getattribute(self, name)

    # Attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls


# 使用实例
@log_getattribute
class TestClassA:
    def __init__(self, x):
        self.x = x

    def spam(self):
        pass


#  the func can statistics the wrapped func run time
def runtime(func):
    @wraps(func)
    def _deco(*args, **kwargs):
        # start time
        start = peer.time.time()
        # executing the original func
        func(*args, **kwargs)
        # end time
        end = peer.time.time()
        print(func.__name__, "executed time:{:.2f}ms".format((end - start) * 1000))

    return _deco


@runtime
def myfunc(x, y):
    for i in range(x, y):
        print(i)


# the func can statistics the wrapped func run time, wrapper with para
def runtime_with_para(para):
    def _deco(func):
        @wraps(func)
        def __deco(*args, **kwargs):
            # start time
            start = peer.time.time()
            # executing the original func
            func(*args, **kwargs)
            # end time
            end = peer.time.time()
            print("The input parameter is:", str(para))
            print(func.__name__, "executed time:{:.2f}ms".format((end - start) * 1000))

        return __deco

    return _deco


@runtime_with_para("China")
def myfunc(x, y):
    for i in range(x, y):
        print(i)


def deco_1(func):
    @wraps(func)
    def _deco_1(*args, **kwargs):
        print("before deco_1 ......")
        func(*args, **kwargs)
        print("after deco_1 ......")

    return _deco_1


def deco_2(func):
    @wraps(func)
    def _deco_2(*args, **kwargs):
        print("before deco_2 ......")
        func(*args, **kwargs)
        print("after deco_2 ......")

    return _deco_2


@deco_1
@deco_2
def my(a, b):
    print("this is the original func!")
    return a * b


# add delay
def rand_sleep_after(func):
    @wraps(func)
    def _deco(*args, **kwargs):
        func(*args, **kwargs)
        peer.time.sleep(randint(10, 30))

    return _deco


def deco_statics_list(func):
    @wraps(func)
    def _deco(*args, **kwargs):
        res = func(*args, **kwargs)
        print(res)
        return res

    return _deco


@deco_statics_list
def count_list(a: list, type: int):
    list_len = len(list(filter(lambda x: x == type, a)))
    return list_len


def is_odd(n):
    return n % 2 == 1


# 组装文本邮件
def package_text_email(mail_msg, mail_from, mail_to, mail_subject) -> MIMEText:
    # 纯文本邮件
    """
    :param mail_msg: the text of the email content:
    :param mail_from: sender of the email:
    :param mail_to: receiver of the email:
    :param mail_subject: subject of the email:
    :return: return the MIMETEXT content of the email:
    """
    msg = MIMEText(mail_msg, "plain", "utf-8")
    msg['From'] = Header(mail_from, 'utf-8')
    msg['To'] = Header(mail_to, 'utf-8')
    msg['Subject'] = Header(mail_subject, 'utf-8')
    return msg


# 组装html邮件
def package_html_email(mail_msg, mail_from, mail_to, mail_subject) -> MIMEText:
    # html邮件
    """
    :param mail_msg: the html of the email content, multi lines html:
    :param mail_from: sender of the email:
    :param mail_to: receiver of the email:
    :param mail_subject: subject of the email:
    :return: return the MIMETEXT content of the email:
    """
    msg = MIMEText(mail_msg, "html", "utf-8")
    msg['From'] = Header(mail_from, 'utf-8')
    msg['To'] = Header(mail_to, 'utf-8')
    msg['Subject'] = Header(mail_subject, 'utf-8')
    return msg


# 组装带附件邮件（一个文件，一张图片）
def package_attach_email(mail_msg, mail_from, mail_to, mail_subject, attachfile, attachimage) -> MIMEMultipart:
    # 纯文本邮件
    """
    :param mail_msg: the html of the email content, multi lines html:
    :param mail_from: sender of the email:
    :param mail_to: receiver of the email:
    :param mail_subject: subject of the email:
    :param attachfile: the file attachment, the whole path of the file:
    :param attachimage: the image attachment, the whole path of the file:
    :return: return the multi parts content of the email:
    """

    # 邮件正文
    message = MIMEText(mail_msg, "html", "utf-8")

    # 创建邮件
    msg = MIMEMultipart()

    # 组装邮件头
    msg['From'] = Header(mail_from, 'utf-8')
    msg['To'] = Header(mail_to, 'utf-8')
    msg['Subject'] = Header(mail_subject, 'utf-8')

    # 组装邮件正文
    msg.attach(message)

    # 构造邮件附件1
    att1 = MIMEText(str(open(attachfile, 'rb').read()), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    # 邮件附件中展示的文件名
    att1['Content-Disposition'] = 'attachment; filename="attachment1" '
    # 组装邮件附件
    msg.attach(att1)

    # 构造邮件附件2 图片
    att2 = MIMEText(str(open(attachimage, 'rb').read()), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    # 邮件附件中展示的文件名
    att2["Content-Disposition"] = "attachment; filename='cctv.jpg'"
    # 组装邮件附件
    msg.attach(att2)

    return msg


# 组装html邮件, html带有
def package_html_image_email(mail_msg_html_image, mail_from, mail_to, mail_subject, attachfile,
                             attachimage) -> MIMEMultipart:
    """
    :param mail_msg_html_image: html 邮件，邮件中只包含1张图片，图片的id为:image1
    html sample:
    <p>Python 邮件发送测试...</p>
    <p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
    <p>图片演示：</p>
    <p><img src="cid:image1"></p>
    :param mail_from:
    :param mail_to:
    :param mail_subject:
    :param attachfile:
    :param attachimage:
    :return:
    """

    message_html_image = MIMEMultipart('related')
    message_html_image['From'] = Header(mail_from, 'utf-8')
    message_html_image['To'] = Header(mail_to, 'utf-8')
    message_html_image['Subject'] = Header(mail_subject, 'utf-8')

    # add email content
    msgalternative = MIMEMultipart('alternative')
    # 将html 加入到邮件正文
    msgalternative.attach(MIMEText(mail_msg_html_image, 'html', 'utf-8'))
    message_html_image.attach(msgalternative)
    # 将图片加载到当前目录
    fp = open(attachimage, 'rb')
    messageimage = MIMEImage(fp.read())
    fp.close()

    # 定义图片ID，在HTML文本中引用
    messageimage.add_header('Content-ID', '<image1>')
    message_html_image.attach(messageimage)

    return message_html_image


# send email sample
def send_qq_email(msg, sender, receiver, username, psd, host="smtp.qq.com"):
    """
    msg: 邮件的内容
    host: SMTP 服务器主机。 你可以指定主机的ip地址或者域名如: run.com，这个是可选参数。
    port: 如果你提供了 host 参数, 你需要指定 SMTP 服务使用的端口号，一般情况下 SMTP 端口号为25。
    """

    try:
        smtp_obj = smtplib.SMTP_SSL(host)
        smtp_obj.login(username, psd)
        smtp_obj.sendmail(sender, receiver, msg.as_string())  # send email
        pause()
        smtp_obj.quit()  # 关闭链接
        print("email has been sent...")
    except peer.e as e:
        print(format(e))
        print("send email failed!")


def send_email_deco(host, port, username, password, sender, receiver, msg):
    try:
        smtp_obj = smtplib.SMTP_SSL(host)  # 发件人邮箱中的SMTP服务器，端口号是465(SSL)/25
        # smtp_obj = smtplib.SMTP()        # smtp创建对象
        # smtp_obj.connect(host, port)     # 连接主机
        smtp_obj.login(username, password)  # 登录smtp服务器
        smtp_obj.sendmail(sender, receiver, msg.as_string())  # 发送邮件
        pause()
        smtp_obj.quit()  # 关闭链接
        print("email has been sent...")
    except peer.e as e:
        print(format(e))
        print("send email failed!")


# IP地址有效性判断
def is_ip(ip):
    if ip is None:
        return False

    num_list = ip.split(".")
    if len(num_list) != 4:
        return False
    for num in num_list:
        if not num.isdigit() or not 0 <= int(num) <= 255:
            return False
    return True


def check_ipv4(in_str):
    ip = in_str.strip().split(".")
    return False if len(ip) != 4 or False in map(lambda x: True if x.isdigit() and 0 <= int(x) <= 255 else False, ip) \
        else True


# switch and case class implement
class Switch(object):
    def __init__(self, case_path):
        self.switch_to = case_path
        self._invoked = False
        self.result = None

    def case(self, key, method):
        if (key == self.switch_to) and (not self._invoked):
            self._invoked = True
            # method()
            self.result = method()
        return self

    def default(self, method):
        if not self._invoked:
            self._invoked = True
            # method()
            self.result = method()
        return self


def cn():
    return 'cn'
    # print('Chinese!')


def us():
    return 'us'
    # print('United States')


def failed():
    return 'unknown'
    # print('unknown')


# a demo for func
def hi(name):
    """
    :param name:
    :return:
    """
    print("now you are inside the hi() function")

    def greet():
        print("now you are in the greet() function")

    def welcome():
        print("now you are in the welcome() function")

    if "Simon" == name:
        return greet()
    else:
        return welcome()


# DataFrame 操作
def insert_data_frame(df, key, value, line_no) -> DataFrame:
    """
    :param df: DataFrame
    :param key: 插入数据的key
    :param value:插入数据对应的value
    :param line_no: line no
    :return: DataFrame
    """
    df.insert(line_no, key, [value])

    # print(df)
    return df


# search in the db, only check 1 colum
def search_in_mysql(dbconfig, table_name, colum_name, colum_vale):
    # create connector
    conn = pymysql.connect(**dbconfig)
    # create cursor
    cursor = conn.cursor()
    # prepare and run the sql
    # sql = 'select id from ' + table_name + ' where ' + colum_name + ' = ' + colum_vale
    sql = 'SELECT id from ' + table_name + ' WHERE ' + colum_name + ' = ' + colum_vale
    num = cursor.execute(sql)
    conn.close()
    # 判断是否有返回结果
    if num > 0:
        return True
    else:
        return False


# search id in the db, only check 1 colum
def get_id_in_mysql(dbconfig, table_name, colum_name, colum_vale) -> int:
    # create connector
    conn = pymysql.connect(**dbconfig)
    # create cursor
    cursor = conn.cursor()
    # prepare and run the sql
    # sql = 'select id from ' + table_name + ' where ' + colum_name + ' = ' + colum_vale
    sql = 'SELECT id from ' + table_name + ' WHERE ' + colum_name + ' = ' + colum_vale
    cursor.execute(sql)
    car_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return car_id


# check the specific 是否存在？ 存在返回id，不存在返回0
def check_car_boss(dbconfig, table_name, cn_list, cv_list) -> int:
    # create connector
    conn = pymysql.connect(**dbconfig)
    # create cursor
    cursor = conn.cursor()
    # prepare and run the sql

    condition = str(cn_list[0]) + '="' + str(cv_list[0]) + '"'
    ln = len(cn_list)
    if len(cn_list) > 1:
        for i in range(1, ln):
            condition = condition + " and " + str(cn_list[i]) + '="' + str(cv_list[i]) + '"'

    sql = 'SELECT id from ' + table_name + ' WHERE ' + condition
    # print(str(sql))
    num = cursor.execute(sql)
    # print(str(num))
    conn.close()
    # 判断是否有返回结果， 有则返回id，无则返回0
    if num > 0:
        return int(cursor.fetchone()[0])
    else:
        return 0


# 检查车商是否重叠
def check_dealer_is_duplicate(dbconfig) -> list:
    # create connector
    conn = pymysql.connect(**dbconfig)
    # create cursor
    cursor = conn.cursor()
    # prepare and run the sql
    sql1 = 'SELECT src from dealer'
    num = cursor.execute(sql1)
    srclist = cursor.fetchall()
    # print(str(num))
    # print(srclist)
    cursor.close()
    if num > 0:
        cursor = conn.cursor()
        for i in range(1, num):
            src = str(srclist[i][0])
            print(src)
            sql2 = 'SELECT id from dealer where src = "' + src + '"'
            num1 = cursor.execute(sql2)
            print(str(num1))
            if num1 > 1:
                print(cursor.fetchone()[0])


# save the data to mysql
def save_dict_to_mysql(connect_engine, table_name, df):
    """
    :param connect_engine:数据库连接引擎，例如:'root:root@127.0.0.1:3306/bank'
    用户名:密码@数据库地址：端口号/数据库
    :param table_name:数据表的名称
    :param df:需要存储的数据，以DataFrame格式存储临时数据
    :return:
    """

    try:
        engine = create_engine('mysql+pymysql://' + connect_engine + '?charset=utf8mb4')
        df.to_sql(table_name, engine, if_exists='append', index=False, index_label=False)
        return True
    except peer.e as e:
        print(format(e))
        return False


# save the data to postgresql
def save_dict_to_postgresql(connect_engine, table_name, df):
    """
    :param connect_engine:数据库连接引擎，例如:'root:root@127.0.0.1:3306/bank'
    用户名:密码@数据库地址：端口号/数据库
    :param table_name:
    :param df:
    :return:
    """
    engine = create_engine('postgresql+psycopg2://' + connect_engine + '?charset=utf8')
    df.to_sql(table_name, engine, if_exists='append', index=False, index_label=False)


connect_engine = 'root:simon001@127.0.0.1:3306/ex_car'
table_name_1 = 'car'

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "simon001",
    "port": 3306,
    "database": "ex_car"
}


def is_substring(st1, sub):
    if sub in st1:
        return True
    else:
        return False

