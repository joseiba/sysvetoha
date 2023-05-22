from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

url = 'http://127.0.0.1:8000/'
class CajaTest(LiveServerTestCase):
    def testCaja(self):
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

        driver.get(url + 'caja/listCajas/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"#add_caja")
        add.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]")
        find.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH, "//*[@id='list_cajas']/tbody/tr/td[8]/button")
        find.click()
        time.sleep(3)

        find = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/button[1]")
        find.click()
        time.sleep(3)
        
        driver.quit