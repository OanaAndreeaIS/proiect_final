import random
import string
import unittest
import time

from selenium import webdriver
from Modul_Autentificare import Authentification


# USE CASE: Ca si utilizator autentificat vreau sa am posibilitatea sa:
##############################################################################################
# test1:
# sa accesez modulul de Assign Leave
# sa depun o cerere de concediu
# Sa o identific
##############################################################################################


class AddAdmin(unittest.TestCase):
    link = "https://opensource-demo.orangehrmlive.com/"

    # definim metoda setUp
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.link)  # accesam site-ul nostru OrangeHRM
        self.driver.maximize_window()  # facem fereastra mare
        self.driver.implicitly_wait(10)  # folosim implicitly wait
        time.sleep(2)

    @staticmethod
    def generate_random_string(length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def write_to_file(data, filename="generated_username.txt"):
        with open(filename, 'w') as file:
            file.write(data)

    @staticmethod
    def read_from_file(filename="generated_username.txt"):
        with open(filename,'r') as file:
            return file.read().strip()

    # definim metoda tearDown
    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def test_adaugare_administrator(self):
        print("Folosim metoda de autentificare din suita de teste Autentificare")
        auth = Authentification()
        auth.driver = self.driver
        auth.authentification()
