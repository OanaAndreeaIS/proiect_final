import unittest
import HtmlTestRunner

from Modul_Autentificare import Authentification

class TestSuite(unittest.TestCase):
    def test_suite(self):
        # Creează o instanță a suitei de teste
        suite = unittest.TestSuite()

        # Adaugă testele din clasa Alert la suită
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Authentification)),

        # Creează un obiect HtmlTestRunner
        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title="Smoke Testing Report",
            report_name="Raport Complet"
        )

        # Rulează testele și generează raportul HTML
        runner.run(suite)