from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from apps.usuario.tests import LoginFormTest
from config.settings import URL_BASE_TEST_FUNTIONAL
# Create your tests here.
class AgendamientosFormTest(LiveServerTestCase):
    def testAddAgendamiento(self):
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

        driver.get(URL_BASE_TEST_FUNTIONAL + 'reserva/listReserva/')
        time.sleep(2)

        ##cambiar en el dia de la evaluacion
        submit = driver.find_element(By.XPATH,"//*[@id='calendar']/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[6]/td[3]")
        submit.click()
        time.sleep(3)

        element = driver.find_element(By.XPATH, "//select[@name='id_servicio']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(1)

        element = driver.find_element(By.XPATH, "//*[@id='id_empleado']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(1)      

        element = driver.find_element(By.XPATH, "//select[@name='id_cliente']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(1)

        element = driver.find_element(By.XPATH, "//select[@name='id_mascota']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(3)      
    
        submit = driver.find_element(By.XPATH,"//*[@id='button_add']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.quit


    # def testEditAgendamiento(self):
    #     driver = webdriver.Chrome()
    #     driver.get(URL_BASE_TEST_FUNTIONAL + 'accounts/login/')

    #     user_name = driver.find_element('name', 'username')
    #     user_password = driver.find_element('name','password')

    #     submit = driver.find_element('id','button_submit')

    #     user_name.send_keys('joseiba')
    #     time.sleep(2)
    #     user_password.send_keys('joseiba')
    #     time.sleep(2)

    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(2)

    #     driver.get(URL_BASE_TEST_FUNTIONAL + 'reserva/listReserva/')
    #     time.sleep(2)

    #     #cambiar en el dia de la evaluacion
    #     submit = driver.find_element(By.XPATH,"//*[@id='calendar']/div[2]/div/table/tbody/tr/td/div/div/div/table/tbody/tr[6]/td[3]")
    #     submit.click()
    #     time.sleep(3)        

    #     element = driver.find_element(By.XPATH, "//select[@name='estado_re']")
    #     all_options = element.find_elements(By.TAG_NAME, "option")
    #     for option in all_options:
    #         option.click()
    #     time.sleep(3)      
    
    #     submit = driver.find_element(By.XPATH,"//*[@id='edit_button']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit


