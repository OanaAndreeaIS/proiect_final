import random
import string
import unittest
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from Modul_Autentificare import Authentification

######################################################################################
# USE CASE: Ca si utilizator autentificat vreau sa am posibilitatea sa:
# editez administratorul
######################################################################################
class EditAdmin(unittest.TestCase):
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
    def test_editare_admin_nou(self):
        print("Folosim metoda de autentificare din suita de teste Autentificare")
        auth = Authentification()
        auth.driver = self.driver
        auth.authentification()

        print("Accesam pagina Admin")
        modul_admin = self.driver.find_element(By.CSS_SELECTOR, "li:nth-of-type(1) > .oxd-main-menu-item")
        modul_admin.click()
        time.sleep(2)

        print("Verificam ca suntem pe pagina de Admini")
        pagina_admin = self.driver.current_url
        assert "index.php/admin/viewSystemUsers" in pagina_admin, "Testul a picat: Nu suntem pe pagina de Admin"
        print("Suntem pe pagina de Admini")
        time.sleep(2)

        # Salvam username-ul din fisier intr-o variabila noua
        username_random = self.read_from_file()
        print("Username din fisier: ",username_random)

        # Cautam dupa username si incepem editarea acestuia
        username_cautare = self.driver.find_element(By.CSS_SELECTOR,
                                                    "[class] .oxd-grid-item--gutters:nth-of-type(1) input")
        username_cautare.send_keys(username_random)
        time.sleep(3)

        buton_cautare = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-left-space")
        buton_cautare.click()
        time.sleep(3)

        rezultate = self.driver.find_element(By.XPATH,
                                             "//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']/div[@class='oxd-layout-context']//span[@class='oxd-text oxd-text--span']")
        rezultate_text = rezultate.text
        assert "Record Found" in rezultate_text, "Testul a picat: Nu s-a identificat adminul nostru"
        print("Am identificat adminul nostru")
        time.sleep(2)

        print("Incepem editarea acestuia")
        buton_editare = self.driver.find_element(By.CSS_SELECTOR,"button:nth-of-type(2) > .bi-pencil-fill.oxd-icon")
        buton_editare.click()
        time.sleep(2)

        print("Verificam ca suntem pe pagina de editare")
        pagina_curenta = self.driver.current_url
        assert "web/index.php/admin/saveSystemUser/" in pagina_curenta,"Testul a picat: Nu suntem pe pagina de editare"
        print("Suntem pe pagina de editare")

        print("Schimbam rolul")
        user_role = self.driver.find_element(By.CLASS_NAME, 'oxd-select-text-input')
        current_role = user_role.text
        print("Rolul curent este: ", current_role)

        # Determinam rolul dorit
        new_role = "ESS" if current_role == "Admin" else "Admin"
        print(f"Schimbam rolul in: {new_role}")

        user_role.click()
        time.sleep(2)
        options = self.driver.find_elements(By.XPATH, "//div[@role='option']")
        for option in options:
            if option.text == new_role:
                option.click()
                break
        time.sleep(2)
        print(f"Rolul s-a modificat in: {new_role}")

        print("Schimbam statusul")
        # Selectam statusul
        status = self.driver.find_element(By.CSS_SELECTOR,
                                          ".oxd-form .oxd-grid-item--gutters:nth-of-type(3) [tabindex]")
        status.click()
        time.sleep(2)
        status.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        status.send_keys(Keys.ENTER)
        print("Status Disabled")
        time.sleep(2)

        # Schimbam username-ul
        username = self.driver.find_element(By.CSS_SELECTOR,".oxd-form-row .oxd-input")
        username.click()
        username.clear()
        time.sleep(2)
        new_username = EditAdmin.generate_random_string()
        username.send_keys(new_username)
        print("Noul username este: ",new_username)
        time.sleep(2)

        # Salvam username-ul in fisier
        self.write_to_file(new_username)

        # Salvam modificarile
        buton_salvare = self.driver.find_element(By.XPATH,"//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']//form[@class='oxd-form']//button[@type='submit']")
        buton_salvare.click()
        time.sleep(4)

        # Verificam ca suntem redirectionati catre pagina de admini
        pagina_curenta = self.driver.current_url
        assert "index.php/admin/viewSystemUsers" in pagina_curenta, "Testul a picat: Nu s-a reusit salvarea noului admin"
        print("Suntem pe pagina adminilor. Acum il vom cauta pe adminul nostru")
        time.sleep(2)

        username_cautare = self.driver.find_element(By.CSS_SELECTOR,
                                                    "[class] .oxd-grid-item--gutters:nth-of-type(1) input")
        username_cautare.send_keys(new_username)
        time.sleep(3)

        buton_cautare = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-left-space")
        buton_cautare.click()
        time.sleep(3)

        rezultate = self.driver.find_element(By.XPATH,
                                             "//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']/div[@class='oxd-layout-context']//span[@class='oxd-text oxd-text--span']")
        rezultate_text = rezultate.text
        assert "Record Found" in rezultate_text, "Testul a picat: Nu s-a identificat adminul nostru"
        print("Avem un rezultat. Adminul a fost editat cu succes")
        time.sleep(2)
