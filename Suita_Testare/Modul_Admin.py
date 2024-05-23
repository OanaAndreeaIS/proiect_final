import unittest
import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from Modul_Autentificare import Authentification

# USE CASE: Ca si utilizator autentificat vreau sa am posibilitatea sa:
##############################################################################################
# test1:
#   sa accesez modulul Admin
#   sa adaug un administrator nou
#   sa filtrez dupa noul admin adaugat
#   sa resetez filtrele
##############################################################################################
# test2:
#   sa editez administratorul
#   sa sterg administratorul

class Administration(unittest.TestCase):
    link = "https://opensource-demo.orangehrmlive.com/"

    # definim metoda setUp
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.link)  # accesam site-ul nostru Etsy
        self.driver.maximize_window()  # facem fereastra mare
        self.driver.implicitly_wait(10)  # folosim implicitly wait
        time.sleep(2)

    # definim metoda tearDown
    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def test_adaugare_administrator(self):
        # Facem o instanta a clasei Authentification si apoi apelam metodele din acea clasa
        auth_instance = Authentification()
        auth_instance.setUp()  # Setam setUp-ul din clasa Authentification
        auth_instance.test_valid_authentification()  # Apelam testul de autentificare