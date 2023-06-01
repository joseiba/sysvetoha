from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from apps.usuario.tests import LoginFormTest

url = 'http://127.0.0.1:8000/'
class ClienteFormTest(LiveServerTestCase):

    # def testCiudadForm(self):
    #     login = LoginFormTest()
    #     login.testLoginForm()
    #     time.sleep(2)

    #     driver = webdriver.Chrome()
    #     driver.get(url + '/configuracion/listCiudades/')
    #     time.sleep(2)

    #     add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-block btn-primary']")
    #     add.send_keys(Keys.RETURN)
    #     time.sleep(2)

    #     nombre = driver.find_element('name', 'nombre_ciudad')
    #     nombre.send_keys('Asuncio test')
    #     time.sleep(1)       

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit

    
    # def testAddClienteForm(self):
    #     login = LoginFormTest()
    #     login.testLoginForm()
    #     time.sleep(2)

    #     driver = webdriver.Chrome()
    #     driver.get(url + '/cliente/listCliente/')
    #     time.sleep(2)

    #     add = driver.find_element('id', 'button_addCliente')
    #     add.send_keys(Keys.RETURN)
    #     time.sleep(2)

    #     nombre = driver.find_element('name', 'nombre_cliente')
    #     nombre.send_keys('joseTest')
    #     time.sleep(1)

    #     apellido = driver.find_element('name', 'apellido_cliente')
    #     apellido.send_keys('test')
    #     time.sleep(1)

    #     cedula = driver.find_element('name', 'cedula')
    #     cedula.send_keys('987654')
    #     time.sleep(1)

    #     telefono = driver.find_element('name', 'telefono')
    #     telefono.send_keys('0961302455')
    #     time.sleep(1)

    #     element = driver.find_element(By.XPATH, "//select[@name='id_ciudad']")
    #     all_options = element.find_elements(By.TAG_NAME, "option")
    #     for option in all_options:
    #         option.click()
    #     time.sleep(1)
        
    #     cedula = driver.find_element('name', 'direccion')
    #     cedula.send_keys('las dunas')
    #     time.sleep(1)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit

    # def testEditForm(self):
    #     login = LoginFormTest()
    #     login.testLoginForm()
    #     time.sleep(2)

    #     driver = webdriver.Chrome()
    #     driver.get(url + '/cliente/listCliente/')
    #     time.sleep(2)

    #     edit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-warning mr-1']")
    #     edit.send_keys(Keys.RETURN)
    #     time.sleep(2)

    #     nombre = driver.find_element('name', 'nombre_cliente')
    #     nombre.send_keys('jose editado test')
    #     time.sleep(2)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     ok = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
    #     ok.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit

    # def testDeleteForm(self):
    #     login = LoginFormTest()
    #     login.testLoginForm()
    #     time.sleep(2)

    #     driver = webdriver.Chrome()
    #     driver.get(url + '/cliente/listCliente/')
    #     time.sleep(2)

    #     edit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-danger']")
    #     edit.send_keys(Keys.RETURN)
    #     time.sleep(2)      

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit

    def testValidationAddClient(self):
        login = LoginFormTest()
        login.testLoginForm()
        time.sleep(2)

        driver = webdriver.Chrome()
        driver.get(url + '/cliente/listCliente/')
        time.sleep(2)

        add = driver.find_element('id', 'button_addCliente')
        add.send_keys(Keys.RETURN)
        time.sleep(2)
        
        submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
        submit.send_keys(Keys.RETURN)
        time.sleep(5)       

        driver.quit