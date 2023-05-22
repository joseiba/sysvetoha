from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#from vetoho.settings import 'http://127.0.0.1:8000/'

class LoginFormTest(LiveServerTestCase):

	def testLoginForm(self):
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
        

class RolesaddFormTest(LiveServerTestCase):
	def testRoleForm(self):		
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

		driver.get('http://127.0.0.1:8000/' + '/usuario/addRol/')
		time.sleep(2)

		nombre = driver.find_element(By.ID, 'id_name')
		nombre.send_keys('Visitante test')
		time.sleep(1)        

		select = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-success btn-sm']")
		select.send_keys(Keys.RETURN)
		time.sleep(3)

		submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
		submit.send_keys(Keys.RETURN)
		time.sleep(3)				

		ok = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
		ok.send_keys(Keys.RETURN)
		time.sleep(3)
		driver.quit	