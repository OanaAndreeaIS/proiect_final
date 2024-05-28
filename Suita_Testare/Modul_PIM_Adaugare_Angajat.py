import random
import string
import unittest
import time
import os
import pyautogui
from selenium.webdriver import Keys

from selenium.webdriver.common.by import By
from selenium import webdriver
from Modul_Autentificare import Authentification


# USE CASE: Ca si utilizator autentificat vreau sa am posibilitatea sa:
##############################################################################################
# test:
#   sa accesez modulul PIM
#   sa adaug un angajat nou
#   sa adaug un avatar angajatului nou
#   sa filtrez dupa noul angajat adaugat
##############################################################################################


class NewEmployee(unittest.TestCase):
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
    def generate_random_number(length=6):
        return ''.join(random.choices('0123456789', k=length))

    @staticmethod
    def write_to_file(data, filename="id.txt"):
        with open(filename, 'w') as file:
            file.write(data)

    @staticmethod
    def read_from_file(filename="id.txt"):
        with open(filename,'r') as file:
            return file.read().strip()

    # definim metoda tearDown
    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def test_adaugare_angajat(self):
        print("Folosim metoda de autentificare din suita de teste Autentificare")
        auth = Authentification()
        auth.driver = self.driver
        auth.authentification()

        print("Accesam modulul PIM")
        modul_pim = self.driver.find_element(By.CSS_SELECTOR,"li:nth-of-type(2) > .oxd-main-menu-item")
        modul_pim.click()
        time.sleep(2)
        pagina_pim = self.driver.current_url
        assert "web/index.php/pim/viewEmployeeList" in pagina_pim,"Testul a picat: Nu s-a deschis modulul PIM"
        print("Am accesat cu succes modulul PIM - Lista Angajatilor")
        time.sleep(2)

        print("Adaugam un nou angajat")
        add_employee_page = self.driver.find_element(By.XPATH,"//div[@id='app']//header[@class='oxd-topbar']//nav[@role='navigation']/ul/li[3]/a[@href='#']")
        add_employee_page.click()
        time.sleep(2)

        pagina_adauga_angajat = self.driver.current_url
        assert "web/index.php/pim/addEmployee" in pagina_adauga_angajat,"Testul a picat: Nu s-a deschis pagina de adaugare angajat"
        print("Suntem pe pagina de adaugare angajat")

        print("Completam Employee Full Name, care contine campuri Required")
        first_name = self.generate_random_string()
        middle_name = self.generate_random_string()
        last_name = self.generate_random_string()

        # First Name
        first_name_input = self.driver.find_element(By.NAME,"firstName")
        first_name_input.send_keys(first_name)
        time.sleep(2)

        # Middle Name
        middle_name_input = self.driver.find_element(By.NAME,"middleName")
        middle_name_input.send_keys(middle_name)
        time.sleep(2)

        # Last Name
        last_name_input = self.driver.find_element(By.NAME,"lastName")
        last_name_input.send_keys(last_name)
        time.sleep(2)

        # Employee ID
        employee_id = self.driver.find_element(By.CSS_SELECTOR,"[class='oxd-grid-2 orangehrm-full-width-grid'] input")
        employee_id.send_keys(Keys.CONTROL + "a")
        employee_id.send_keys(Keys.DELETE)
        time.sleep(2)
        id = self.generate_random_number()
        self.write_to_file(id)
        employee_id.send_keys(id)
        time.sleep(3)

        # Vreau sa incarc o imagine
        buton_incarca_imagine = self.driver.find_element(By.CSS_SELECTOR,".bi-plus")
        buton_incarca_imagine.click()
        time.sleep(2)

        cale_imagine = "C:\\Users\\atudo\\OneDrive\\Desktop\\Proiect final\\proiect_final\\Suita_Testare\\avatar.jpg"

        # Verificam daca fisierul exista
        if os.path.exists(cale_imagine):
            # Verificam extensia fisierului
            extensie = os.path.splitext(cale_imagine)[1].lower()
            if extensie not in ['.jpg', '.jpeg', '.png', '.gif']:
                print("Tipul de fișier nu este acceptat. Se acceptă doar fișiere JPG, PNG și GIF.")
            else:
                # Verificam dimensiunile fisierului
                dimensiune = os.path.getsize(cale_imagine)
                if dimensiune > 1048576:  # 1MB = 1048576 bytes
                    print("Mărimea fișierului este prea mare. Se acceptă fișiere de maxim 1MB.")
                else:
                    # Transmit calea catre fisierul imagine catre fereastra pop-up
                    pyautogui.write(cale_imagine)
                    pyautogui.press("enter")
        else:
            print("Fișierul specificat nu există.")

        print("Salvam noul utilizator")
        buton_salvare = self.driver.find_element(By.CSS_SELECTOR,".oxd-button--secondary")
        buton_salvare.click()
        time.sleep(3)

        print("Accesam lista angajatilor si cautam angajatul nostru")
        lista_angajati =self.driver.find_element(By.XPATH,"//div[@id='app']//header[@class='oxd-topbar']//nav[@role='navigation']/ul/li[2]")
        lista_angajati.click()
        time.sleep(4)

        camp_cautare =self.driver.find_element(By.CSS_SELECTOR,".orangehrm-full-width-grid.oxd-grid-4 .oxd-input")
        camp_cautare.send_keys(id)
        time.sleep(2)

        buton_cautare = self.driver.find_element(By.CSS_SELECTOR,".orangehrm-left-space")
        buton_cautare.click()
        time.sleep(3)

        rezultate = self.driver.find_element(By.XPATH,
                                             "//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']/div[@class='oxd-layout-context']//span[@class='oxd-text oxd-text--span']")
        rezultate_text = rezultate.text
        assert "Record Found" in rezultate_text, "Testul a picat: Nu s-a identificat angajatul nostru"
        print("Avem un rezultat. Angajatul a fost adaugat cu succes")
        time.sleep(2)
