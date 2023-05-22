from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#from vetoho.settings import 'http://127.0.0.1:8000/'

class FacturasFormTest(LiveServerTestCase):
    
    def testAddFacturaForm(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/' + 'accounts/login/')

        user_name = driver.find_element('name', 'username')
        user_password = driver.find_element('name','password')

        submit = driver.find_element('id','button_submit')

        user_name.send_keys('joseiba')
        time.sleep(2)
        user_password.send_keys('joseiba')
        time.sleep(2)

        submit.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/' + 'ventas/listFacturasVentas/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        add.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH,'/html/body/div/div[1]/section[2]/div/div/form/div/div/div[1]/div[1]/div/div/div[1]/span')
        find.click()
        time.sleep(2)

        find = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
        find.send_keys('ped')
        time.sleep(3)      

        find = driver.find_element(By.XPATH, "//*[@id='select2-search-results']/li")
        find.click()
        time.sleep(3)

        chech = driver.find_element(By.XPATH, '/html/body/div/div[1]/section[2]/div/div/form/div/div/div[1]/div[2]/div/div/div[1]/div/div[1]/input')
        chech.click()
        time.sleep(2)

        element = driver.find_element(By.XPATH, "//select[@name='id_cliente']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(1)

        submit = driver.find_element(By.CSS_SELECTOR,"#button_registrar")
        submit.click()
        time.sleep(3)

        submit = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[6]/button[1]")
        submit.click()
        time.sleep(3)

        driver.quit   