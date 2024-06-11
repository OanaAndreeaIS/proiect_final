# Proiect Final Orange HRM 
## Descriere proiect
OrangeHRM Live Demo este o platformă online destinată testării și explorării funcționalităților oferite de OrangeHRM, un sistem de management al resurselor umane open-source. Website-ul permite utilizatorilor să se familiarizeze cu diversele module și caracteristici ale OrangeHRM într-un mediu controlat și sigur.
## Link către platformă: https://opensource-demo.orangehrmlive.com/

### Framework utilizat
Am utilizat framework-ul Unittest.

### Librării utilizate
- Librăria Selenium 
- HTMLTestRunner
- PyAutoGUI

Testele s-au bazat pe modulele de Autentificare, Administrare Admini, PIM ( înregistrare angajat) și Concediu

S-au folosit metode statice , functii de adaugare , editare, stergere , cautare, salvare în fișiere, citire din fișiere
### Limbaj de programare utilizat
Python

Descriere:
Python este un limbaj de programare interpretat, de nivel înalt, cu o sintaxă clară și concisă, orientat către creșterea productivității dezvoltatorilor și lizibilității codului.

Python poate fi descărcat și instalat de pe site-ul oficial python.org. Comanda tipică pentru a instala un pachet folosind pip.

Managerul de pachete Python, este:

    pip install numele_pachetului

### IDE

PyCharm

Descriere:

PyCharm este un mediu integrat de dezvoltare (IDE) dezvoltat de JetBrains, destinat în special pentru limbajul de programare Python. 

### Instalare librării
Selenium

    pip install selenium

Descriere - _Selenium este o suită de instrumente pentru automatizarea browser-elor web. Permite controlul programatic al unui browser pentru a naviga pe site-uri web, a interacționa cu elemente de pagină și a verifica comportamente specifice_

HTMLTestRunner

    pip install html-testRunner

Descriere - _HTMLTestRunner este un modul pentru Python care extinde funcționalitatea unittest pentru a genera rapoarte de testare în format HTML. Acesta este util pentru a vizualiza rezultatele testelor într-un mod organizat și ușor de citit, oferind informații detaliate despre fiecare test, inclusiv starea acestuia (reușit/eșuat), mesajele de eroare și durata de execuție._

PyAutoGUI

    pip install pyautogui

Descriere - _PyAutoGUI este o bibliotecă Python folosită pentru automatizarea interacțiunilor cu interfața grafică a utilizatorului (GUI). Aceasta permite controlul mișcărilor mouse-ului, apăsărilor de taste, capturii de ecran și altele, fără a depinde de driveri specifici de browser sau alte componente._

### Instalare proiect

Pentru a instala corect proiectul pe mediul local, vor trebui urmați pașii de mai jos:

1. Clonare proiect pe mediul local
2. Deschidere proiect în PyCharm prin apăsare File -> Open -> Selectare proiect din locația unde s-a clonat proiectul
3. Pentru execuția testelor trebuie instalate librăriile selenium, pyautogui și html-testRunner
4. După finalizarea instalării librăriilor se va executa fișierul _run_tests.py_
5. După execuție, raportul poate fi deschis din folderul _reports_ 
6. Pentru o vizualizare mai bună a raportului, se va deschide utilizând browser-ul sugerat în dreapta.