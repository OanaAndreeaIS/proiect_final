import unittest
import HtmlTestRunner

from Modul_Autentificare import Authentification
from Modul_Admin_Adauga import AddAdmin
from Modul_Admin_Editare import EditAdmin
from Modul_Admin_Stergere import DeleteAdmin

class TestSuite(unittest.TestCase):
    def test_suite(self):
        # Creează o instanță a suitei de teste
        suite = unittest.TestSuite()

        # Adaugă testele din clasa Alert la suită
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Authentification)),
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(AddAdmin)),
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(EditAdmin)),
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(DeleteAdmin)),

        # Creează un obiect HtmlTestRunner
        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title="Smoke Testing Report",
            report_name="Raport Complet"
        )

        # Rulează testele și generează raportul HTML
        runner.run(suite)