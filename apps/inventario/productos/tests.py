from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from apps.usuario.tests import LoginFormTest
from config.settings import URL_BASE_TEST_FUNTIONAL

class InventarioFormTest(LiveServerTestCase):
    
    def testAddInventarioForm(self):
        driver = webdriver.Chrome()
        driver.get(URL_BASE_TEST_FUNTIONAL + 'accounts/login/')

        user_name = driver.find_element('name', 'username')
        user_password = driver.find_element('name','password')

        submit = driver.find_element('id','button_submit')

        user_name.send_keys('joseiba')
        time.sleep(2)
        user_password.send_keys('joseiba')
        time.sleep(2)

        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        driver.get(URL_BASE_TEST_FUNTIONAL + 'producto/list_ajustar_inventario/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"body > div > div.content-wrapper > section.content > div > div > div > div > div.card-header > button.btn.btn-primary.float-right.mr-1")
        add.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH, "/html/body/div/div[1]/section[2]/div/div/div/div/div/form/div/div[1]/div/div/div/div[1]/span/span")
        find.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
        find.send_keys('ped')
        time.sleep(3)

        find = driver.find_element(By.XPATH, "//*[@id='select2-search-results']/li")
        find.click()
        time.sleep(3)

        find = driver.find_element(By.XPATH, "//*[@id='tblAjuste']/tbody/tr/td[5]/div/input").clear()
        find = driver.find_element(By.XPATH, "//*[@id='tblAjuste']/tbody/tr/td[5]/div/input")
        find.send_keys('110')
        time.sleep(3)

        add = driver.find_element(By.XPATH, "/html/body/div/div[1]/section[2]/div/div/div/div/div/form/div/div[2]/button")
        add.click()
        time.sleep(3)

        submit = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[4]/div[2]/button")
        submit.click()
        time.sleep(4)
        
        driver.quit
