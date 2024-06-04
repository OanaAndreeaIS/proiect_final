import datetime
import random
import string
import unittest
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys

from Modul_Autentificare import Authentification
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta


# USE CASE: Ca si utilizator autentificat vreau sa am posibilitatea sa:
##############################################################################################
# test:
# sa accesez modulul de Assign Leave
# sa depun o cerere de concediu
# Sa o identific
##############################################################################################


class AssignLeave(unittest.TestCase):
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
    def read_from_file(filename="employee_name.txt"):
        with open(filename, 'r') as file:
            return file.read().strip()

    # definim metoda tearDown
    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def test_adaugam_cerere(self):
        print("Folosim metoda de autentificare din suita de teste Autentificare")
        auth = Authentification()
        auth.driver = self.driver
        auth.authentification()

        print("Accesam pagina Leave, apoi Assign Leave")
        leave_page = self.driver.find_element(By.CSS_SELECTOR, "li:nth-of-type(3) > .oxd-main-menu-item")
        leave_page.click()
        time.sleep(2)

        current_page = self.driver.current_url
        assert "/leave/viewLeaveList" in current_page, "Testul a picat: Nu suntem pe pagine de Leave"
        print("Suntem pe lista cu Concedii")

        assign_leave_page = self.driver.find_element(By.XPATH,
                                                     "//div[@id='app']//header[@class='oxd-topbar']//nav[@role='navigation']/ul/li[7]")
        assign_leave_page.click()
        time.sleep(2)

        current_page_assign_leave = self.driver.current_url
        assert "leave/assignLeave" in current_page_assign_leave, "Testul a picat: Nu suntem pe pagina de Solicitari concedii"
        print("Suntem pe pagina de solicitari concedii")

        print("Completam campurile: Employee name, Leave type , From To Date, Duration")

        # Employee name
        employee_name = self.driver.find_element(By.CSS_SELECTOR,
                                                 ".oxd-autocomplete-text-input > input[placeholder='Type for hints...']")
        employee = self.read_from_file()
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

        # From date - selectam ziua curenta
        calendar = self.driver.find_element(By.CSS_SELECTOR,
                                            "[class] .oxd-grid-item--gutters:nth-of-type(1) [placeholder='yyyy-dd-mm']")
        calendar.click()
        time.sleep(2)

        current_date = datetime.now().day
        current_date_element = self.driver.find_element(By.XPATH, f"//div[text()='{current_date}']")
        current_date_element.click()
        time.sleep(2)
        print("Current date:", current_date)

        # To Date - selectam ziua urmatoare
        calendar_to_date = self.driver.find_element(By.CSS_SELECTOR,
                                                    "[class] .oxd-grid-item--gutters:nth-of-type(2) [placeholder]")
        calendar_to_date.click()
        time.sleep(2)
        calendar_to_date.send_keys(Keys.CONTROL + "a")
        time.sleep(2)
        calendar_to_date.send_keys(Keys.DELETE)
        time.sleep(2)

        current_date_now = datetime.now()
        next_day = current_date_now + timedelta(days=3)
        day_format = next_day.strftime("%Y-%d-%m")
        calendar_to_date.clear()
        time.sleep(2)
        calendar_to_date.send_keys(day_format)
        time.sleep(2)
        calendar_to_date.click()
        time.sleep(2)
        print("To date:", day_format)
        comments = self.driver.find_element(By.CSS_SELECTOR, "textarea")
        comments.click()

        # Partial Duration
        print("Partial Duration")
        dropdown = self.driver.find_element(By.XPATH,
                                            "//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']/div[@class='oxd-layout-context']//form[@class='oxd-form']/div[4]/div//div[@class='oxd-select-wrapper']/div")
        dropdown.click()
        time.sleep(2)
        duration_option = self.driver.find_element(By.XPATH,
                                                   "//div[@class='oxd-select-option' and span[text()='All Days']]")
        duration_option.click()
        time.sleep(2)

        # Duration
        print("Duration")
        duration_list = self.driver.find_element(By.XPATH,
                                                 "//div[@id='app']/div[@class='oxd-layout']/div[@class='oxd-layout-container']/div[@class='oxd-layout-context']//form[@class='oxd-form']/div[4]/div/div[2]/div//div[@class='oxd-select-wrapper']/div[1]//i")
        duration_list.click()
        time.sleep(2)

        duration_opt = self.driver.find_element(By.XPATH,
                                                "//div[@class='oxd-select-option' and span[text()='Half Day - Morning']]")
        duration_opt.click()
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(2)
        # Assign
        print("Assign button")
        buton_assign = self.driver.find_element(By.CSS_SELECTOR, ".oxd-button--secondary")
        buton_assign.click()
        time.sleep(2)

        print("Verificam daca a fost un succes sau angajatul nu are suficiente zile pentru concediu")
        try:
            succes_message = self.driver.find_element(By.XPATH,
                                                      "//div[@id='oxd-toaster_1']/div[@class='oxd-toast oxd-toast--success oxd-toast-container--toast']")
            succes_message_text = succes_message.text.strip()
            print(succes_message_text)
        except NoSuchElementException:
            try:
                confirm_pop_up = self.driver.find_element(By.CSS_SELECTOR,
                                                      "[class='oxd-text oxd-text--p oxd-text--subtitle-2']")
                confirm_pop_up_text = confirm_pop_up.text.strip()
                mesaj = "Employee does not have sufficient leave balance for leave request. Click OK to confirm leave assignment."
                if mesaj in confirm_pop_up_text:
                    print("Nu avem zile suficiente pentru concediu. Apasam ok")
                    buton_ok = self.driver.find_element(By.CSS_SELECTOR, ".oxd-button--secondary.orangehrm-button-margin")
                    buton_ok.click()
                    time.sleep(2)
                else:
                    print("Cererea de concediu s-a creat cu succes!")
            except NoSuchElementException:
                self.fail("Niciun mesaj de confirmare si nicio fereastra de pop-up nu a aparut!")
