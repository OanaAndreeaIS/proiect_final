import unittest
import HtmlTestRunner

from Modul_Autentificare import Authentification
from Modul_Admin_Adauga import AddAdmin
from Modul_Admin_Editare import EditAdmin
from Modul_Admin_Stergere import DeleteAdmin
from Modul_PIM_Adaugare_Angajat import NewEmployee
from Modul_Assign_Leave import AssignLeave
from Modul_Leave_Entitlements import Entitlements

class TestSuite(unittest.TestCase):
    def test_suite(self):
        # Creează o instanță a suitei de teste
        suite = unittest.TestSuite()

        # Adaugă testele din clasa Alert la suită
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Authentification))
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(AddAdmin))
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(EditAdmin))
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DeleteAdmin))
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(NewEmployee))
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Entitlements))
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(AssignLeave))

        # Creează un obiect HtmlTestRunner
        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title="Raport de Testare Aplicatie Web OrangeHRM",
            report_name="Raport Complet"
        )

        # Rulează testele și generează raportul HTML
        runner.run(suite)