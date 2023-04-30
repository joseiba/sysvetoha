from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from apps.usuario.tests import LoginFormTest
from config.settings import URL_BASE_TEST_FUNTIONAL

class ProveedoresFormTest(LiveServerTestCase):
    
    def testAddProveedoresForm(self):
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
        driver.get(URL_BASE_TEST_FUNTIONAL + 'compra/listProveedor/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary float-right']")
        add.click()
        time.sleep(4)

        nombre = driver.find_element('name', 'nombre_proveedor')
        nombre.send_keys('lucas test')
        time.sleep(1)

        direccion = driver.find_element('name', 'direccion')
        direccion.send_keys('las dunas')
        time.sleep(1)

        ruc = driver.find_element('name', 'ruc_proveedor')
        ruc.send_keys('987654')
        time.sleep(1)

        telefono = driver.find_element('name', 'telefono')
        telefono.send_keys('0961302455')
        time.sleep(1)

        email = driver.find_element('name', 'email')
        email.clear()
        email = driver.find_element('name', 'email')
        email.send_keys('test@gmail.com')
        time.sleep(1)        

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.quit

    def testEditProveedoresForm(self):
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
        driver.get(URL_BASE_TEST_FUNTIONAL + 'compra/listProveedor/')
        time.sleep(2)

        edit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-warning mr-1']")
        edit.click()
        time.sleep(2)

        nombre = driver.find_element('name', 'nombre_proveedor')
        nombre.clear()

        nombre = driver.find_element('name', 'nombre_proveedor')
        nombre.send_keys('lucas test')
        time.sleep(1)       

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.quit


    def testDeleteForm(self):
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
        driver.get(URL_BASE_TEST_FUNTIONAL + 'compra/listProveedor/')
        time.sleep(2)

        edit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-danger']")
        edit.send_keys(Keys.RETURN)
        time.sleep(2)      

        submit = driver.find_element(By.CSS_SELECTOR,"#eliminacion > div > div > form > div.modal-footer > button.btn.btn-danger")
        submit.click()
        time.sleep(3)

        driver.quit