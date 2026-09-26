import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from poupe_mais import __version__
from poupe_mais.cli import main


class TestVersao(unittest.TestCase):
    def test_mostra_a_versao_do_sistema(self):
        saida = io.StringIO()
        with redirect_stdout(saida), self.assertRaises(SystemExit) as fim:
            main(["--versao"])
        self.assertEqual(fim.exception.code, 0)
        self.assertEqual(saida.getvalue().strip(), f"Poupe+ {__version__}")


class TestComandos(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = str(Path(self.pasta.name) / "dados.json")

    def tearDown(self):
        self.pasta.cleanup()

    def executar(self, *argumentos):
        saida, erros = io.StringIO(), io.StringIO()
        with redirect_stdout(saida), redirect_stderr(erros):
            codigo = main(["--arquivo", self.arquivo, *argumentos])
        return codigo, saida.getvalue(), erros.getvalue()

    def test_registra_lancamentos_e_mostra_saldo(self):
        self.executar("receita", "3000", "Salário", "-c", "Salário", "-d", "05/09/2026")
        self.executar("despesa", "1250.50", "Aluguel", "-c", "Moradia", "-d", "10/09/2026")
        codigo, saida, _ = self.executar("saldo")
        self.assertEqual(codigo, 0)
        self.assertIn("R$ 1.749,50", saida)

    def test_lista_so_os_lancamentos_do_mes_pedido(self):
        self.executar("despesa", "30", "Pizza", "-c", "lazer", "-d", "31/08/2026")
        self.executar("despesa", "45.90", "Almoço", "-c", "alimentação", "-d", "18/09/2026")
        codigo, saida, _ = self.executar("listar", "--mes", "09/2026")
        self.assertEqual(codigo, 0)
        self.assertIn("Almoço", saida)
        self.assertIn("Alimentação", saida)
        self.assertIn("-R$ 45,90", saida)
        self.assertNotIn("Pizza", saida)

    def test_valor_negativo_mostra_erro_e_nao_grava(self):
        codigo, _, erros = self.executar("despesa", "-10", "Estorno")
        self.assertEqual(codigo, 1)
        self.assertIn("maior que zero", erros)
        self.assertFalse(Path(self.arquivo).exists())


if __name__ == "__main__":
    unittest.main()
