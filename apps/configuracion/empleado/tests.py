from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from apps.usuario.tests import LoginFormTest
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
        	
        driver.get(URL_BASE_TEST_FUNTIONAL + '/configuracion/listEmpleado/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-block btn-primary']")
        add.send_keys(Keys.RETURN)
        time.sleep(2)

        nombre_emp = driver.find_element('name', 'nombre_emp')
        nombre_emp.send_keys('Jose test')
        time.sleep(1)

        apellido_emp = driver.find_element('name', 'apellido_emp')
        apellido_emp.send_keys('Lopez test')
        time.sleep(1)

        ci_empe = driver.find_element('name', 'ci_empe')
        ci_empe.send_keys('369852')
        time.sleep(1)             

        element = driver.find_element(By.XPATH, "//select[@name='id_servicio']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(1)

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        ok = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
        ok.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.quit

