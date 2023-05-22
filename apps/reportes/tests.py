from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

url = 'http://127.0.0.1:8000/'
class ReporteTest(LiveServerTestCase):
    def testViewReport(self):
        driver = webdriver.Chrome()
        driver.get(url + 'accounts/login/')

        user_name = driver.find_element('name', 'username')
        user_password = driver.find_element('name','password')

        submit = driver.find_element('id','button_submit')

        user_name.send_keys('joseiba')
        time.sleep(2)
        user_password.send_keys('joseiba')
        time.sleep(2)

        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        driver.get(url + 'reporte/listServiciosVendidos/')
        time.sleep(4)

        driver.get(url + 'reporte/listReporteProductoVendidos/')
        time.sleep(4)

        driver.quit