from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#from vetoho.settings import 'http://127.0.0.1:8000/'

class MAscotasFormTest(LiveServerTestCase):
    # def testEspecieForm(self):        
    #     driver = webdriver.Chrome()
    #     driver.get('http://127.0.0.1:8000/' + 'accounts/login/')
		
    #     user_name = driver.find_element('name', 'username')
    #     user_password = driver.find_element('name','password')

    #     submit = driver.find_element('id','button_submit')

    #     user_name.send_keys('joseiba')
    #     time.sleep(2)
    #     user_password.send_keys('joseiba')
    #     time.sleep(2)

    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(2)	

    #     driver.get('http://127.0.0.1:8000/' + '/mascota/listEspecie/')
    #     time.sleep(2)

    #     add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary float-right']")
    #     add.send_keys(Keys.RETURN)
    #     time.sleep(2)

    #     nombre = driver.find_element('name', 'nombre_especie')
    #     nombre.send_keys('Canino test')
    #     time.sleep(1)        

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit

    # def testRazaForm(self):       

    #     driver = webdriver.Chrome()
    #     driver.get('http://127.0.0.1:8000/' + 'accounts/login/')

    #     user_name = driver.find_element('name', 'username')
    #     user_password = driver.find_element('name','password')

    #     submit = driver.find_element('id','button_submit')

    #     user_name.send_keys('joseiba')
    #     time.sleep(2)
    #     user_password.send_keys('joseiba')
    #     time.sleep(2)

    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(2)	


    #     driver.get('http://127.0.0.1:8000/' + '/mascota/listRaza/')
    #     time.sleep(2)

    #     add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary float-right']")
    #     add.send_keys(Keys.RETURN)
    #     time.sleep(2)

    #     nombre = driver.find_element('name', 'nombre_raza')
    #     nombre.send_keys('Pitbull Test')
    #     time.sleep(1)    
        
    #     element = driver.find_element(By.XPATH, "//select[@name='id_especie']")
    #     all_options = element.find_elements(By.TAG_NAME, "option")
    #     for option in all_options:
    #         option.click()
    #     time.sleep(1)    

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit


    def testMascotaForm(self):
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

        driver.get('http://127.0.0.1:8000/' + '/mascota/add/')
        time.sleep(2)

        nombre = driver.find_element('name', 'nombre_mascota')
        nombre.send_keys('Keisy')
        time.sleep(1)

        
        peso = driver.find_element('name', 'peso')
        peso.send_keys('500')
        time.sleep(1)                
        
        element = driver.find_element(By.XPATH, "//select[@name='id_raza']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(1)    

        element = driver.find_element(By.XPATH, "//select[@name='id_cliente']")
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


    # def testEditForm(self):
    #     driver = webdriver.Chrome()
    #     driver.get('http://127.0.0.1:8000/' + 'accounts/login/')

    #     user_name = driver.find_element('name', 'username')
    #     user_password = driver.find_element('name','password')

    #     submit = driver.find_element('id','button_submit')

    #     user_name.send_keys('joseiba')
    #     time.sleep(2)
    #     user_password.send_keys('joseiba')
    #     time.sleep(2)

    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(2)

    #     driver.get('http://127.0.0.1:8000/' + 'mascota/edit/1/')
    #     time.sleep(2)

    #     # submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-outline-primary ml-3 mr-3 mb-3']")
    #     # submit.send_keys(Keys.RETURN)
    #     # time.sleep(3)

    #     nombre = driver.find_element('name', 'nombre_mascota')
    #     nombre.clear()
    #     time.sleep(1)       

    #     nombre_edit = driver.find_element('name', 'nombre_mascota')
    #     nombre_edit.send_keys('keisy editado')
    #     time.sleep(1)       

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit


