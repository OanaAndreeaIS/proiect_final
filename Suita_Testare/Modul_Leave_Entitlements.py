import unittest
import time

from selenium import webdriver
from Modul_Autentificare import Authentification
from selenium.webdriver.common.by import By


# USE CASE: Ca si utilizator autentificat vreau sa am posibilitatea sa:
##############################################################################################
# test:
# sa accesez modulul Leave - Entitlements - Employee Entitlements
# sa inregistrez zile de concediu de drept
# sa sterg zilele de concediu de drept
##############################################################################################

class Entitlements(unittest.TestCase):
    link = "https://opensource-demo.orangehrmlive.com/"

    # definim metoda setUp
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.link)  # accesam site-ul nostru OrangeHRM
        self.driver.maximize_window()  # facem fereastra mare
        self.driver.implicitly_wait(10)  # folosim implicitly wait
        time.sleep(2)

    @staticmethod
    def read_from_file(filename="employee_name.txt"):
        with open(filename, 'r') as file:
            return file.read().strip()

    # definim metoda tearDown
    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def test_adaugam_zile_de_drept(self):
        print("Folosim metoda de autentificare din suita de teste Autentificare")
        auth = Authentification()
        auth.driver = self.driver
        auth.authentification()

        print("Accesam modulul Leave - Entitlements - Employee Entitlements")
        leave = self.driver.find_element(By.XPATH, "//div[@id='app']//aside[@class='oxd-sidepanel']/nav[@role='navigation']//ul[@class='oxd-main-menu']/li[3]")
        leave.click()
        time.sleep(2)

        entitlements = self.driver.find_element(By.XPATH, "//div[@id='app']//header[@class='oxd-topbar']//nav[@role='navigation']/ul/li[3]")
        entitlements.click()
        time.sleep(2)

        employee_entitlements = self.driver.find_element(By.XPATH,
                                                         "//div[@id='app']//div[@class='oxd-topbar-body']/nav[@role='navigation']/ul/li[3]/ul[@role='menu']/li[2]")
        employee_entitlements.click()
        time.sleep(2)

        page = self.driver.current_url
        assert "/leave/viewLeaveEntitlements" in page, "Testul a picat:Nu suntem pe pagina de Employee Entitlements"
        print("Suntem pe pagina Employee Entitlements")

        print("Introducem Employee Name")
        employee = self.read_from_file()
        employee_name = self.driver.find_element(By.CSS_SELECTOR,
                                                 ".oxd-autocomplete-text-input > input[placeholder='Type for hints...']")
        employee_name.send_keys(employee)
        time.sleep(2)
        optiune_employee = self.driver.find_elements(By.XPATH, "//div[@role='listbox']")

        for opt in optiune_employee:
            print(opt.text)
        for opt in optiune_employee:
            if opt.text == employee:
                opt.click()
                break
        time.sleep(2)
        print("Employee Name:", employee)

        # Apasam butonul de Search
        search_button = self.driver.find_element(By.CSS_SELECTOR, ".oxd-button--secondary")
        search_button.click()

        print("Verificam daca avem cereri depuse pentru Dreptul la concediu")
        tabel = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-horizontal-padding")
        tabel_text = tabel.text.strip()
        if "No Records Found" in tabel_text:
            print("Nu avem cereri depuse. Depunem o cerere")
            button_add = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-header-container .oxd-button--secondary")
            button_add.click()
            time.sleep(2)
            pagina_curenta = self.driver.current_url
            assert "leave/addLeaveEntitlement" in pagina_curenta, "Testul a picat: Nu suntem pe pagina de adaugare o cerere Concediu de drept"
            print("Suntem pe pagina de adaugare cerere concediu de drept")
            time.sleep(2)

            # Employee Name
            print("Introducem Employee Name")
            employee = self.read_from_file()
            employee_name = self.driver.find_element(By.CSS_SELECTOR,
                                                     ".oxd-autocomplete-text-input > input[placeholder='Type for hints...']")
            employee_name.send_keys(employee)
            time.sleep(2)
            optiune_employee = self.driver.find_elements(By.XPATH, "//div[@role='listbox']")

            for opt in optiune_employee:
                print(opt.text)
            for opt in optiune_employee:
                if opt.text == employee:
                    opt.click()
                    break
            time.sleep(2)
            print("Employee Name:", employee)

            # Leave Type
            leave_type = self.driver.find_element(By.CSS_SELECTOR, ".oxd-select-text-input")
            leave_type.click()
            time.sleep(2)
            optiune = self.driver.find_element(By.XPATH, "//div[@class='oxd-select-option']/span[text()='CAN - FMLA']")
            optiune.click()
            time.sleep(2)

            # Entitlement
            entitlement_input = self.driver.find_element(By.XPATH,
                                                         "//div[@id='app']//form[@class='oxd-form']/div[3]/div/div[3]/div//input")
            entitlement_input.send_keys("21")

            # Save
            save_button = self.driver.find_element(By.CSS_SELECTOR, ".oxd-button--secondary")
            save_button.click()
            time.sleep(2)

            # Confirmam noua cerere
            confirm_button = self.driver.find_element(By.CSS_SELECTOR, ".oxd-button--secondary.orangehrm-button-margin")
            confirm_button.click()
            time.sleep(2)

            print("Verificam ca s-a adaugat noua cerere pentru concediul de drept")
            tabel_continut = self.driver.find_element(By.CSS_SELECTOR, ".orangehrm-horizontal-padding")
            tabel_continut_text = tabel_continut.text
            assert "(1) Record Found" in tabel_continut_text, "Testul a picat: Nu s-a adaugat cererea"
            print("Avem o inregistrare. Testarea se opreste.")
        else:
            print("Avem cereri depuse. Testarea se opreste")
            return
