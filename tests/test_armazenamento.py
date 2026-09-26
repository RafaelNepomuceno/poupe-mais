import json
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from poupe_mais import armazenamento
from poupe_mais.carteira import Carteira
from poupe_mais.modelos import TipoLancamento


class TestArmazenamento(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = Path(self.pasta.name) / "dados.json"

    def tearDown(self):
        self.pasta.cleanup()

    def test_arquivo_inexistente_gera_carteira_vazia(self):
        self.assertEqual(armazenamento.carregar(self.arquivo).lancamentos(), [])

    def test_salva_e_carrega_os_mesmos_lancamentos(self):
        carteira = Carteira()
        carteira.registrar(TipoLancamento.RECEITA, Decimal("2500.00"), "Salário", "Salário", date(2026, 9, 5))
        carteira.registrar(TipoLancamento.DESPESA, Decimal("186.35"), "Conta de luz", "Contas", date(2026, 9, 8))
        armazenamento.salvar(carteira, self.arquivo)

        recarregada = armazenamento.carregar(self.arquivo)
        self.assertEqual(recarregada.lancamentos(), carteira.lancamentos())

    def test_valores_sao_gravados_como_texto_para_nao_perder_centavos(self):
        carteira = Carteira()
        carteira.registrar(TipoLancamento.DESPESA, Decimal("0.10"), "Bala", data=date(2026, 9, 1))
        armazenamento.salvar(carteira, self.arquivo)

        dados = json.loads(self.arquivo.read_text(encoding="utf-8"))
        self.assertEqual(dados["versao_formato"], armazenamento.VERSAO_FORMATO)
        self.assertEqual(dados["lancamentos"][0]["valor"], "0.10")


if __name__ == "__main__":
    unittest.main()
