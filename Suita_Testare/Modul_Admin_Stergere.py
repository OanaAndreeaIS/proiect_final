import random
import string
import unittest
import time


from selenium.webdriver.common.by import By
from selenium import webdriver
from Modul_Autentificare import Authentification

######################################################################################
# USE CASE: Ca si utilizator autentificat vreau sa am posibilitatea:
#   sa sterg administratorul
######################################################################################
class DeleteAdmin(unittest.TestCase):
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
    def test_delete_admin(self):
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
        new_username = self.read_from_file()
        print("Username din fisier: ", new_username)

        # Cautam dupa username si incepem stergerea acestuia
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
        print("Am identificat adminul nostru")
        time.sleep(2)

        print("Apasam butonul de stergere")
        buton_stergere = self.driver.find_element(By.CSS_SELECTOR,".bi-trash")
        buton_stergere.click()
        time.sleep(2)

        fereastra_pop_up = self.driver.find_element(By.XPATH,"//div[@id='app']/div[@role='dialog']//div[@role='document']/div[@class='orangehrm-text-center-align']/p")
        fereastra_text = fereastra_pop_up.text.strip()
        expected_text = "The selected record will be permanently deleted. Are you sure you want to continue?"
        assert expected_text == fereastra_text,"Testul a picat: Nu s-a deschis fereastra pop-up de stergere"
        print("The selected record will be permanently deleted. Are you sure you want to continue?")
        time.sleep(2)

        buton_yes = self.driver.find_element(By.CSS_SELECTOR,".oxd-button--label-danger")
        buton_yes.click()
        time.sleep(2)

        rezultate = self.driver.find_element(By.XPATH,
                                             "//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']/div[@class='oxd-layout-context']//span[@class='oxd-text oxd-text--span']")
        rezultate_text = rezultate.text
        assert "No Records Found" in rezultate_text, "Testul a picat: S-a identificat adminul nostru. Nu s-a sters"
        print("Nu am identificat adminul nostru.Acesta a fost sters cu succes")
        time.sleep(2)

