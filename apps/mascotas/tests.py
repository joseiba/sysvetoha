from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from apps.usuario.tests import LoginFormTest
from vetoho.settings import URL_BASE_TEST_FUNTIONAL

class MAscotasFormTest(LiveServerTestCase):
    def testEspecieForm(self):
        login = LoginFormTest()
        login.testLoginForm()
        time.sleep(2)

        driver = webdriver.Chrome()
        driver.get(URL_BASE_TEST_FUNTIONAL + '/mascota/listEspecie/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary float-right']")
        add.send_keys(Keys.RETURN)
        time.sleep(2)

        nombre = driver.find_element('name', 'nombre_especie')
        nombre.send_keys('Canino test')
        time.sleep(1)        

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.quit

    def testRazaForm(self):
        login = LoginFormTest()
        login.testLoginForm()
        time.sleep(2)

        driver = webdriver.Chrome()
        driver.get(URL_BASE_TEST_FUNTIONAL + '/mascota/listRaza/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary float-right']")
        add.send_keys(Keys.RETURN)
        time.sleep(2)

        nombre = driver.find_element('name', 'nombre_raza')
        nombre.send_keys('Pitbull Test')
        time.sleep(1)    
        
        element = driver.find_element(By.XPATH, "//select[@name='id_especie']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(1)    

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.quit
