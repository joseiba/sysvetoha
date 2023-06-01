from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

#from config.settings import 'http://127.0.0.1:8000/'
url = 'http://127.0.0.1:8000/'
class LoginFormTest(LiveServerTestCase):

	def testLoginForm(self):
		driver = webdriver.Chrome()
		
		driver.get(url + 'accounts/login/')
		
		user_name = driver.find_element('name', 'username')
		user_password = driver.find_element('name','password')

		submit = driver.find_element('id','button_submit')

		user_name.send_keys('joseiba')
		time.sleep(2)
		user_password.send_keys('joseiba')
		time.sleep(2)

		submit.send_keys(Keys.RETURN)
		time.sleep(2)		        
        

# class RolesaddFormTest(LiveServerTestCase):
# 	def testRoleForm(self):		
# 		driver = webdriver.Chrome()
		
# 		driver.get(url + 'accounts/login/')
		
# 		user_name = driver.find_element('name', 'username')
# 		user_password = driver.find_element('name','password')

# 		submit = driver.find_element('id','button_submit')

# 		user_name.send_keys('joseiba')
# 		time.sleep(2)
# 		user_password.send_keys('joseiba')
# 		time.sleep(2)

# 		submit.send_keys(Keys.RETURN)
# 		time.sleep(2)	

# 		driver.get(url + '/usuario/addRol/')
# 		time.sleep(2)

# 		nombre = driver.find_element(By.ID, 'id_name')
# 		nombre.send_keys('Visitante test')
# 		time.sleep(1)        

# 		select = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-success btn-sm']")
# 		select.send_keys(Keys.RETURN)
# 		time.sleep(3)

# 		submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
# 		submit.send_keys(Keys.RETURN)
# 		time.sleep(3)				

# 		ok = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
# 		ok.send_keys(Keys.RETURN)
# 		time.sleep(3)
# 		driver.quit	

class UsuarioTestForm(LiveServerTestCase):
	def testAddUser(self):
		driver = webdriver.Chrome()
		
		driver.get(url + 'accounts/login/')
		
		user_name = driver.find_element('name', 'username')
		user_password = driver.find_element('name','password')

		submit = driver.find_element('id','button_submit')

		user_name.send_keys('joseiba')
		time.sleep(2)
		user_password.send_keys('joseiba')
		time.sleep(2)

		submit.send_keys(Keys.RETURN)
		time.sleep(2)

		driver.get(url + '/usuario/listUsuarios/')
		time.sleep(2)

		add = driver.find_element(By.CSS_SELECTOR,"body > div > div.content-wrapper > section.content > div > div > div > div > div.card-header > div.float-right > button.btn.btn-primary.btn-circle > a")
		add.send_keys(Keys.RETURN)
		time.sleep(2)

		selectRol = driver.find_element(By.XPATH,"/html/body/div/div[1]/section[2]/div/div/div/div/div/div/form/div[1]/div/p[1]/span[1]/span[1]/span/span/textarea")
		selectRol.click()
		time.sleep(2)

		selectRol = driver.find_element(By.XPATH,"/html/body/span/span/span/ul/li[1]")
		selectRol.click()
		time.sleep(2)

		nombreUser = driver.find_element(By.XPATH, '//*[@id="id_username"]')
		nombreUser.send_keys('joseiba')
		#nombreUser.send_keys('adminjoseiba')
		time.sleep(1)

		nombre = driver.find_element(By.XPATH, '//*[@id="id_first_name"]')
		nombre.send_keys('julio test')
		time.sleep(1)

		aepllido = driver.find_element(By.XPATH, '//*[@id="id_last_name"]')
		aepllido.send_keys('gonzales test')
		time.sleep(1)  

		email = driver.find_element(By.XPATH, '//*[@id="email"]')
		email.send_keys('test@gmail.com')
		time.sleep(1)

		pass1 = driver.find_element(By.XPATH, '//*[@id="id_password1"]')
		pass1.send_keys('passTest398p2')
		time.sleep(1)

		pass2 = driver.find_element(By.XPATH, '//*[@id="id_password2"]')
		#pass2.send_keys('passTest398p2')
		pass2.send_keys('passTest398p')
		time.sleep(1)

		submit = driver.find_element(By.XPATH,"/html/body/div/div[1]/section[2]/div/div/div/div/div/div/form/div[2]/button[1]")
		submit.click()
		time.sleep(5)

		driver.quit




