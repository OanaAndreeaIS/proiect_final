import random
import string
import unittest
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver

# USE CASE: Ca si utilizator vreau sa am posibilitatea sa:
# accesez site-ul Etsy
# sa incerc sa ma inregistrez cu o adresa de email invalida si o parola corecta
# sa incerc sa ma inregistrez cu o adresa de email valida si o parola incorecta


class InvalidRegistration(unittest.TestCase):
    link = "https://www.etsy.com/"

    # definim metoda setUp
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.link) # accesam site-ul nostru Etsy
        self.driver.maximize_window() # facem fereastra mare
        self.driver.implicitly_wait(10) # folosim implicitly wait

        # Verificam daca apare CAPTCHA
        try:
            captcha_header = self.driver.find_element(By.XPATH,
                                                      "//div[@id='captcha-container']/div[@class='captcha__header']")
            print("CAPTCHA a fost detectat. Facem refresh la pagina.")
            self.driver.refresh()
            time.sleep(2)
        except NoSuchElementException:
            print("CAPTCHA nu a fost detectat. Continuam cu testul.")

        print("Acceptam cookies")
        accept_cookies = self.driver.find_element(By.XPATH,"/html//div[@id='gdpr-single-choice-overlay']//button[@class='wt-btn wt-btn--filled wt-mb-xs-0']")
        accept_cookies.click()
        time.sleep(2)

    # definm metoda tearDown
    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def generate_random_email(self):
        email_len = 10
        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=email_len)) + "@exemplu.com"
        return email

    def generate_random_string(self, length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def test_invalid_registration(self):
        print("Apasam butonul Sign in pentru a ajunge la fereastra de inregistrare")
        sign_in = self.driver.find_element(By.XPATH,"//header[@id='gnav-header-inner']/div[@class='wt-flex-shrink-xs-0']/nav/ul//button[1]")
        sign_in.click()
        time.sleep(2)

        print("Verificam faptul ca s-a deschis fereastra pentru Sign in")
        fereastra_sign_in = self.driver.find_element(By.XPATH,"/html//h1[@id='join-neu-overlay-title']")
        fereastra_sign_in_text = fereastra_sign_in.text
        assert "Sign in" in fereastra_sign_in_text,"Testul a picat: Nu s-a deschis fereastra de sign-in"
        print("Fereastra de Sign in s-a deschis. Continuam cu testul de inregistrare")
        time.sleep(2)

        print("Identificam butonul de inregistrare si facem click pe acesta")
        buton_register = self.driver.find_element(By.XPATH,"/html//form[@id='join-neu-form']//div[@class='wt-grid__item-xs-12']/div[1]//button[@type='button']")
        buton_register.click()
        time.sleep(2)

        print("Verificam ca s-a schimbat fereastra din Sign in in Create your account")
        fereastra_creare_cont = self.driver.find_element(By.XPATH,"/html//h1[@id='join-neu-overlay-title']")
        fereastra_creare_cont_text = fereastra_creare_cont.text
        assert "Create your account" in fereastra_creare_cont_text,"Testul a picat: Nu s-a deschis fereastra de creare cont"
        print("Suntem pe fereastra de creare cont")
        time.sleep(2)

        print("Incepem procesul de inregistrare cont print completarea invalida a adresei de email: ")
        print("Email address")
        print("First name")
        print("Password")

        # Generam datele necesare pentru inregistrare
        invalid_random_email = "test"
        random_first_name = self.generate_random_string()
        valid_random_password = self.generate_random_string(12)

        # Email address
        adresa_email = self.driver.find_element(By.ID,"join_neu_email_field")
        adresa_email.send_keys(invalid_random_email)
        time.sleep(2)

        # First name
        first_name = self.driver.find_element(By.ID,"join_neu_first_name_field")
        first_name.send_keys(random_first_name)
        time.sleep(2)

        # Password
        password = self.driver.find_element(By.ID,"join_neu_password_field")
        password.send_keys(valid_random_password)
        time.sleep(2)

        # Buton Register
        register = self.driver.find_element(By.NAME,"submit_attempt")
        register.click()
        time.sleep(2)

        print("Verificam ca nu s-a reusit autentificarea si ca a aparut mesajul de avertizare email incorect")
        fereastra_creare_cont = self.driver.find_element(By.XPATH, "/html//h1[@id='join-neu-overlay-title']")
        fereastra_creare_cont_text = fereastra_creare_cont.text
        assert "Create your account" in fereastra_creare_cont_text, "Testul a picat: Nu s-a deschis fereastra de creare cont"
        print("Suntem tot pe fereastra de creare cont")
        time.sleep(2)

        mesaj_eroare_prezent = self.driver.find_element(By.ID,"aria-join_neu_email_field-error").text
        assert "Please enter a valid email address." in mesaj_eroare_prezent,"Testul a picat: Mesajul de avertizare email incorect absent"
        print("Testul a trecut: Mesajul de avertizare email incorect, prezent")
        time.sleep(2)

        # Stergem ceea ce am scris in campuri
        adresa_email.clear()
        first_name.clear()
        password.clear()
        time.sleep(2)

        print("Incepem procesul de inregistrare cont print completarea invalida a parolei: ")
        print("Email address")
        print("First name")
        print("Password")

        # Generam datele necesare pentru inregistrare
        valid_random_email = self.generate_random_email()
        random_first_name = self.generate_random_string()
        invalid_random_password = "abc"

        # Email address
        adresa_email = self.driver.find_element(By.ID, "join_neu_email_field")
        adresa_email.send_keys(valid_random_email)
        time.sleep(2)

        # First name
        first_name = self.driver.find_element(By.ID, "join_neu_first_name_field")
        first_name.send_keys(random_first_name)
        time.sleep(2)

        # Password
        password = self.driver.find_element(By.ID, "join_neu_password_field")
        password.send_keys(invalid_random_password)
        time.sleep(2)

        # Buton Register
        register = self.driver.find_element(By.NAME, "submit_attempt")
        register.click()
        time.sleep(2)

        print("Verificam ca nu s-a reusit autentificarea si ca a aparut mesajul de avertizare email incorect")
        fereastra_creare_cont = self.driver.find_element(By.XPATH, "/html//h1[@id='join-neu-overlay-title']")
        fereastra_creare_cont_text = fereastra_creare_cont.text
        assert "Create your account" in fereastra_creare_cont_text, "Testul a picat: Nu s-a deschis fereastra de creare cont"
        print("Suntem tot pe fereastra de creare cont")
        time.sleep(2)

        mesaj_eroare_prezent = self.driver.find_element(By.ID, "aria-join_neu_password_field-error").text
        assert "Must be at least 6 characters." in mesaj_eroare_prezent, "Testul a picat: Mesajul de avertizare parola incorecta absent"
        print("Testul a trecut: Mesajul de avertizare parola incorecta, prezent")
        time.sleep(2)







