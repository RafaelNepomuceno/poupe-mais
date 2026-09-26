import io
import unittest
from contextlib import redirect_stdout

from poupe_mais import __version__
from poupe_mais.cli import main


class TestVersao(unittest.TestCase):
    def test_mostra_a_versao_do_sistema(self):
        saida = io.StringIO()
        with redirect_stdout(saida), self.assertRaises(SystemExit) as fim:
            main(["--versao"])
        self.assertEqual(fim.exception.code, 0)
        self.assertEqual(saida.getvalue().strip(), f"Poupe+ {__version__}")


if __name__ == "__main__":
    unittest.main()
