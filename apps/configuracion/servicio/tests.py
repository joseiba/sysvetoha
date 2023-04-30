from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from apps.usuario.tests import LoginFormTest, login
from config.settings import URL_BASE_TEST_FUNTIONAL

class ServicioFormTest(LiveServerTestCase):

    def testServicioForm(self):
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
        time.sleep(2)

        driver.get(URL_BASE_TEST_FUNTIONAL + '/configuracion/listServicio/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-block btn-primary']")
        add.send_keys(Keys.RETURN)
        time.sleep(2)

        nombre = driver.find_element('name', 'nombre_servicio')
        nombre.send_keys('Consulta test')
        time.sleep(1)

        precio_servicio = driver.find_element('name', 'precio_servicio')
        precio_servicio.send_keys('25000')
        time.sleep(1)

        min_serv = driver.find_element('name', 'min_serv')
        min_serv.send_keys('30')
        time.sleep(1)     

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        ok = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
        ok.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.quit
