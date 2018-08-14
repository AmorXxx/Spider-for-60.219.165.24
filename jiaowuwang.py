from selenium import webdriver
from MySQLCommand import MySQLCommand


browser = webdriver.Chrome()
browser.get('http://60.219.165.24')

mysqlCommand = MySQLCommand()
mysqlCommand.connectMysql()
#这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
dataCount = int(mysqlCommand.getLastId()) + 1

for i in range(2016026751,2018039999):
    username = browser.find_element_by_name('zjh')
    username.send_keys(i)
    username = browser.find_element_by_name('mm')
    username.send_keys('1')
    btn = browser.find_element_by_id('btnSure')
    btn.click()
    if browser.find_elements_by_class_name('errorTop'):
        continue
    else:
        try:
            browser.switch_to.frame(browser.find_element_by_xpath("//frame[@src='/menu/s_top.jsp']"))
            st = '学生'
        except Exception:
            browser.switch_to.frame(browser.find_element_by_xpath("//frame[@src='/menu/t_top.jsp']"))
            st = '教师'


    btn_logout = browser.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[2]/table/"
                                               "tbody/tr[1]/td/table/tbody/tr/td/a")
    name = browser.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[2]/table/tbody"
                                         "/tr[1]/td/table/tbody/tr/td")
    news_dict = {
        "id": str(dataCount),
        "name": name.text[6:-6],
        "idcard": str(i),

    }
    try:
        # 插入数据，如果已经存在就不在重复插入
        res = mysqlCommand.insertData(news_dict)
        if res:
            dataCount = res
    except Exception as e:
        print("插入数据失败", str(e))  # 输出插入失败的报错语句





    btn_logout.click()
    browser.switch_to.alert.accept()
    continue
browser.quit()
