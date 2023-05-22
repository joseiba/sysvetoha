from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

url = 'http://127.0.0.1:8000/'
#class ProveedoresFormTest(LiveServerTestCase):
    # def testAddProveedoresForm(self):
    #     driver = webdriver.Chrome()
    #     driver.get(url + 'accounts/login/')

    #     user_name = driver.find_element('name', 'username')
    #     user_password = driver.find_element('name','password')

    #     submit = driver.find_element('id','button_submit')

    #     user_name.send_keys('joseiba')
    #     time.sleep(2)
    #     user_password.send_keys('joseiba')
    #     time.sleep(2)

    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(2)
    #     driver.get(url + 'compra/listProveedor/')
    #     time.sleep(2)

    #     add = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary float-right']")
    #     add.click()
    #     time.sleep(4)

    #     nombre = driver.find_element('name', 'nombre_proveedor')
    #     nombre.send_keys('lucas test')
    #     time.sleep(1)

    #     direccion = driver.find_element('name', 'direccion')
    #     direccion.send_keys('las dunas')
    #     time.sleep(1)

    #     ruc = driver.find_element('name', 'ruc_proveedor')
    #     ruc.send_keys('987654')
    #     time.sleep(1)

    #     telefono = driver.find_element('name', 'telefono')
    #     telefono.send_keys('0961302455')
    #     time.sleep(1)

    #     email = driver.find_element('name', 'email')
    #     email.clear()
    #     email = driver.find_element('name', 'email')
    #     email.send_keys('test@gmail.com')
    #     time.sleep(1)        

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit

    # def testEditProveedoresForm(self):
    #     driver = webdriver.Chrome()
    #     driver.get(url + 'accounts/login/')

    #     user_name = driver.find_element('name', 'username')
    #     user_password = driver.find_element('name','password')


    #     submit = driver.find_element('id','button_submit')

    #     user_name.send_keys('joseiba')
    #     time.sleep(2)
    #     user_password.send_keys('joseiba')
    #     time.sleep(2)

    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(2)
    #     driver.get(url + 'compra/listProveedor/')
    #     time.sleep(2)

    #     edit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-warning mr-1']")
    #     edit.click()
    #     time.sleep(2)

    #     nombre = driver.find_element('name', 'nombre_proveedor')
    #     nombre.clear()

    #     nombre = driver.find_element('name', 'nombre_proveedor')
    #     nombre.send_keys('lucas test')
    #     time.sleep(1)       

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     submit = driver.find_element(By.CSS_SELECTOR,"button[class='swal2-confirm swal2-styled swal2-default-outline']")
    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(3)

    #     driver.quit

    # def testDeleteForm(self):
    #     driver = webdriver.Chrome()
    #     driver.get(url + 'accounts/login/')

    #     user_name = driver.find_element('name', 'username')
    #     user_password = driver.find_element('name','password')


    #     submit = driver.find_element('id','button_submit')

    #     user_name.send_keys('joseiba')
    #     time.sleep(2)
    #     user_password.send_keys('joseiba')
    #     time.sleep(2)

    #     submit.send_keys(Keys.RETURN)
    #     time.sleep(2)
    #     driver.get(url + 'compra/listProveedor/')
    #     time.sleep(2)

    #     edit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-danger']")
    #     edit.send_keys(Keys.RETURN)
    #     time.sleep(2)      

    #     submit = driver.find_element(By.CSS_SELECTOR,"#eliminacion > div > div > form > div.modal-footer > button.btn.btn-danger")
    #     submit.click()
    #     time.sleep(3)

    #     driver.quit

class PedidosComprasTest(LiveServerTestCase):
    def testPedidosCompras(self):
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

        driver.get(url + 'compra/listPedidosCompra/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"body > div > div.content-wrapper > section.content > div > div > div > div > div.card-header > div.float-right > button")
        add.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/div[2]/div/div/div[2]/form/div/div/div/div/div[1]/div[1]/span/span")
        find.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
        find.send_keys('anti')
        time.sleep(3)

        find = driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul/li")
        find.click()
        time.sleep(3)
       
        submit = driver.find_element(By.CSS_SELECTOR,"#add_pedido_compra")
        submit.click()
        time.sleep(4)

        submit = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[6]/button[1]")
        submit.click()
        time.sleep(4)
        
        driver.quit

    def testEditPedidosCompras(self):
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

        driver.get(url + 'compra/listPedidosCompra/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"#list_pedidos > tbody > tr.odd > td:nth-child(3) > button.btn.btn-warning > a")
        add.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH, "//*[@id='tblPedido']/tbody/tr/td[4]/div/input").clear()
        find = driver.find_element(By.XPATH, "//*[@id='tblPedido']/tbody/tr/td[4]/div/input")
        find.send_keys('10')
        time.sleep(3)      
       
        submit = driver.find_element(By.CSS_SELECTOR,"#edit_compra_pedido")
        submit.click()
        time.sleep(4)

        submit = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[6]/button[1]")
        submit.click()
        time.sleep(4)
        
        driver.quit    

class FacturaCompraTest(LiveServerTestCase):
    def testAddFacturaCompra(self):
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

        driver.get(url + 'compra/listFacturasCompras/')
        time.sleep(2)

        add = driver.find_element(By.CSS_SELECTOR,"body > div > div.content-wrapper > section.content > div > div > div > div > div > div.float-right > button")
        add.click()
        time.sleep(4)

        find = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper > div.content-wrapper > div > div > div.row > div > div > div.x_content > form > div > div.row > div.col-lg-9 > div > div > div.form-group > span > span > span.selection > span")
        find.click()
        time.sleep(4)

        find = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
        find.send_keys('anti')
        time.sleep(3)

        find = driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul/li")
        find.click()
        time.sleep(3)

        tim = driver.find_element(By.CSS_SELECTOR, "#id_nro_timbrado")
        tim.send_keys("885454435-5")
        time.sleep(3)

        fac = driver.find_element(By.CSS_SELECTOR, "#id_nro_factura")
        fac.send_keys("25")
        time.sleep(3)

        element = driver.find_element(By.XPATH, "//select[@name='id_proveedor']")
        all_options = element.find_elements(By.TAG_NAME, "option")
        for option in all_options:
            option.click()
        time.sleep(2)

        fecha_ini = driver.find_element(By.CSS_SELECTOR, "#datePick-emision")
        fecha_ini.click()
        time.sleep(3)

        selec_fecha_ini = driver.find_element(By.XPATH, "//*[@id='ui-datepicker-div']/table/tbody/tr[1]/td[4]/a")
        selec_fecha_ini.click()
        time.sleep(3)

        fecha_fin = driver.find_element(By.CSS_SELECTOR, "#datePick-vencimiento")
        fecha_fin.click()
        time.sleep(3)

        selec_fecha_fin = driver.find_element(By.XPATH, "//*[@id='ui-datepicker-div']/table/tbody/tr[5]/td[3]/a")
        selec_fecha_fin.click()
        time.sleep(3)

        submit = driver.find_element(By.CSS_SELECTOR,"#button_factura")
        submit.click()
        time.sleep(4)

        submit = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[6]/button[1]")
        submit.click()
        time.sleep(4)
        
        driver.quit
