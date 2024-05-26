import random
import string
import unittest
import time

from selenium.webdriver import Keys
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

    @staticmethod
    def generate_random_string(length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    # definim metoda tearDown
    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def test_adaugare_administrator(self):
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

        print("Adaugam un administrator nou")
        buton_add = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-header-container .oxd-button--secondary")
        buton_add.click()
        time.sleep(2)

        # Verificam ca suntem pe pagina de adaugare admin
        add_admin = self.driver.current_url
        assert "index.php/admin/saveSystemUser" in add_admin, "Nu s-a deschis pagina de adaugare admin"
        print("Suntem pe pagina de adaugare admin nou")

        print(
            "Completam campurile obligatorii necesare inscrierii unui nou admin: User Role, Employee Name, Status, Username, Password, Confirm Password")
        # Selectam User Role din lista derulanta
        user_role = self.driver.find_element(By.CLASS_NAME, 'oxd-select-text')
        user_role.click()
        time.sleep(2)

        optiuni = self.driver.find_elements(By.XPATH, "//div[@role='option']")

        # Iteram prin optiuni si selectam Admin
        for option in optiuni:
            print(option.text)
        for option in optiuni:
            if option.text == "Admin":
                option.click()
                break
        time.sleep(3)

        # Selectam Employee Name
        empployee_name = self.driver.find_element(By.XPATH, "//input[@placeholder='Type for hints...']")
        empployee_name.send_keys("Timothy Lewis Amiano")
        time.sleep(2)
        optiune_timothy = self.driver.find_elements(By.XPATH, "//div[@role='listbox']")

        for opt in optiune_timothy:
            print(opt.text)
        for opt in optiune_timothy:
            if opt.text == "Timothy Lewis Amiano":
                opt.click()
                break
        time.sleep(2)

        # Selectam statusul
        status = self.driver.find_element(By.CSS_SELECTOR,
                                          ".oxd-form .oxd-grid-item--gutters:nth-of-type(3) [tabindex]")
        status.click()
        time.sleep(2)
        status.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        status.send_keys(Keys.ENTER)
        print("Status Enabled")
        time.sleep(2)

        # Username
        username = self.driver.find_element(By.XPATH,
                                            "//input[@class='oxd-input oxd-input--active' and @autocomplete='off']")
        random_username = Administration.generate_random_string()
        print("Random username: ", random_username)
        username.send_keys(random_username)
        time.sleep(2)

        # Password
        password = self.driver.find_element(By.XPATH,
                                            "//div[@id='app']//form[@class='oxd-form']/div[@class='oxd-form-row user-password-row']/div/div[@class='oxd-grid-item oxd-grid-item--gutters user-password-cell']/div//input[@type='password']")
        password.send_keys("Test135!")
        time.sleep(2)

        # Confirm Password
        confirm_password = self.driver.find_element(By.CSS_SELECTOR, ".oxd-grid-item--gutters:nth-of-type(2) [type]")
        confirm_password.send_keys("Test135!")
        time.sleep(2)

        # Salvam
        print("Salvam")
        buton_salvare = self.driver.find_element(By.XPATH,
                                                 "//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']//form[@class='oxd-form']//button[@type='submit']")
        buton_salvare.click()
        time.sleep(5)

        # Verificam ca suntem redirectionati catre pagina de admini
        pagina_curenta = self.driver.current_url
        assert "index.php/admin/viewSystemUsers" in pagina_curenta, "Testul a picat: Nu s-a reusit salvarea noului admin"
        print("Suntem pe pagina adminilor. Acum il vom cauta pe adminul nostru")
        time.sleep(2)

        username_cautare = self.driver.find_element(By.CSS_SELECTOR,
                                                    "[class] .oxd-grid-item--gutters:nth-of-type(1) input")
        username_cautare.send_keys(random_username)
        time.sleep(3)

        buton_cautare = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-left-space")
        buton_cautare.click()
        time.sleep(3)

        rezultate = self.driver.find_element(By.XPATH,
                                             "//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']/div[@class='oxd-layout-context']//span[@class='oxd-text oxd-text--span']")
        rezultate_text = rezultate.text
        assert "Record Found" in rezultate_text, "Testul a picat: Nu s-a identificat adminul nostru"
        print("Avem un rezultat. Adminul a fost adaugat cu succes")
        time.sleep(2)
