import random
import string
import unittest
import time

from selenium.webdriver.common.by import By
from selenium import webdriver


# USE CASE: Ca si utilizator vreau sa am posibilitatea sa:
##############################################################################################
# test1:
#   accesez site-ul https://opensource-demo.orangehrmlive.com/
#   sa ma autentific cu succes
#   sa ma deloghez cu succes
##############################################################################################
# test2:
#   campurile username si parola sunt campuri obligatorii si mesajele de eroare sunt prezente
##############################################################################################
# test3:
#   username correct
#   password incorect
#
#   username incorrect
#   password correct
#
#   username incorrect
#   password incorrect


class Authentification(unittest.TestCase):
    link = "https://opensource-demo.orangehrmlive.com/"

    # definim variabilele
    username = "Admin"
    password = "admin123"

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

    def generate_random_string(self, length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def authentification(self):
        print("Verificam faptul ca suntem pe pagina de autentificare a site-ului")
        fereastra_autentificare = self.driver.current_url
        assert "index.php/auth/login" in fereastra_autentificare, "Testul a picat: Nu s-a deschis fereastra de creare cont"
        print("Suntem pe fereastra de creare cont")
        time.sleep(2)

        print("Incepem procesul de autentificare utilizand credentialele furnizate de website")

        # Introducem informatiile in campurile obligatorii
        # Username
        username_input = self.driver.find_element(By.NAME, "username").send_keys(self.username)
        time.sleep(2)

        # Password
        password_input = self.driver.find_element(By.NAME, "password").send_keys(self.password)
        time.sleep(2)

        # Apasam butonul de Login
        buton_login = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-login-button").click()
        time.sleep(2)

        print("Verificam ca suntem pe prima pagina")
        prima_pagina = self.driver.current_url
        assert "index.php/dashboard/index" in prima_pagina, "Testul a picat: Autentificarea nu s-a reusit"
        print("Testul a trecut: Suntem pe prima pagina!")
        time.sleep(2)

    def test_valid_authentification(self):
        self.authentification()

    def test_logout(self):
        self.test_valid_authentification()
        time.sleep(2)

        print("Ne delogam")
        buton_drop_down = self.driver.find_element(By.XPATH, "//span[@class='oxd-userdropdown-tab']")
        buton_drop_down.click()
        time.sleep(2)

        buton_delogare = self.driver.find_element(By.XPATH,
                                                  "//ul[@class='oxd-dropdown-menu']//a[contains(text(),'Logout')]")
        buton_delogare.click()
        time.sleep(2)

        print("Verificam ca ne-am delogat cu succes si suntem pe pagina de autentificare")
        pagina_curenta = self.driver.current_url
        assert "web/index.php/auth/login" in pagina_curenta, "Testul a picat: Nu am reusit delogarea"
        print("Testul a trecut: Ne-am delogat cu succes!")

    def test_required_fields_authentification(self):
        print("Verificam faptul ca suntem pe pagina de autentificare a site-ului")
        fereastra_autentificare = self.driver.current_url
        assert "index.php/auth/login" in fereastra_autentificare, "Testul a picat: Nu s-a deschis fereastra de creare cont"
        print("Suntem pe fereastra de creare cont")
        time.sleep(2)

        print(
            "Verificam daca cele doua campuri sunt ambele campuri obligatorii prin apasarea butonului Login fara a introduce credentialele")
        # Apasam butonul de Login
        buton_login = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-login-button")
        buton_login.click()
        time.sleep(2)

        print("Verificam daca s-a reusit autentificarea si daca avem prezente mesajele de eroare")
        pagina_curenta = self.driver.current_url
        assert "web/index.php/auth/login" in pagina_curenta, "Testul a picat: Autentificarea s-a reusit fara ca cele doua campuri sa fie completate"
        print("Testul a trecut: Nu s-a reusit autentificarea")
        time.sleep(2)

        username = self.driver.find_element(By.XPATH, "//input[@name='username']")
        # Verificam daca este required
        if 'oxd-input--error' in username.get_attribute('class'):
            print("Campul username este marcat ca si required")
        else:
            print("Testul a picat: Nu avem campul username marcat ca si required")
        time.sleep(2)

        password = self.driver.find_element(By.XPATH, "//input[@name='password']")
        # Verificam daca este required
        if 'oxd-input--error' in password.get_attribute('class'):
            print("Campul password este marcat ca si required")
        else:
            print("Testul a picat: Nu avem campul password marcat ca si required")
        time.sleep(2)

    def test_invalid_authentification(self):
        print("Verificam faptul ca suntem pe pagina de autentificare a site-ului")
        fereastra_autentificare = self.driver.current_url
        assert "index.php/auth/login" in fereastra_autentificare, "Testul a picat: Nu s-a deschis fereastra de creare cont"
        print("Suntem pe fereastra de creare cont")
        time.sleep(2)

        print("Incepem procesul de autentificare utilizand credentialele incorecte")

        # Introducem informatiile in campurile obligatorii
        #   username correct
        #   password incorect

        # Username correct
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys(self.username)
        time.sleep(2)

        # Password incorrect
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(self.generate_random_string())
        time.sleep(2)

        # Apasam butonul de Login
        buton_login = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-login-button")
        buton_login.click()
        time.sleep(2)

        print("Verificam ca avem prezent mesajul de eroare autentificarea")
        mesaj_avertizare = self.driver.find_element(By.XPATH,"//div[@class='oxd-alert-content oxd-alert-content--error']")
        mesaj_avertizare_text = mesaj_avertizare.text
        assert "Invalid credentials" in mesaj_avertizare_text,"Testul a picat: Nu este prezent mesajul de avertizare"
        print("Invalid credentials!")
        time.sleep(2)

        #   username incorrect
        #   password corect

        # Username incorrect
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys(self.generate_random_string())
        time.sleep(2)

        # Password correct
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(self.password)
        time.sleep(2)

        # Apasam butonul de Login
        buton_login = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-login-button")
        buton_login.click()
        time.sleep(2)

        print("Verificam ca avem prezent mesajul de eroare autentificarea")
        mesaj_avertizare = self.driver.find_element(By.XPATH,
                                                    "//div[@class='oxd-alert-content oxd-alert-content--error']")
        mesaj_avertizare_text = mesaj_avertizare.text
        assert "Invalid credentials" in mesaj_avertizare_text, "Testul a picat: Nu este prezent mesajul de avertizare"
        print("Invalid credentials!")
        time.sleep(2)

        #   username incorrect
        #   password incorrect

        # Username incorrect
        username_input = self.driver.find_element(By.NAME, "username")
        username_input.send_keys(self.generate_random_string())
        time.sleep(2)

        # Password incorrect
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(self.generate_random_string())
        time.sleep(2)

        # Apasam butonul de Login
        buton_login = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-login-button")
        buton_login.click()
        time.sleep(2)

        print("Verificam ca avem prezent mesajul de eroare autentificarea")
        mesaj_avertizare = self.driver.find_element(By.XPATH,
                                                    "//div[@class='oxd-alert-content oxd-alert-content--error']")
        mesaj_avertizare_text = mesaj_avertizare.text
        assert "Invalid credentials" in mesaj_avertizare_text, "Testul a picat: Nu este prezent mesajul de avertizare"
        print("Invalid credentials!")
        time.sleep(2)