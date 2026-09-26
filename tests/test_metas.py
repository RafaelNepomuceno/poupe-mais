import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from poupe_mais import armazenamento
from poupe_mais.carteira import Carteira
from poupe_mais.formatacao import barra_de_progresso, formatar_percentual
from poupe_mais.modelos import Meta


class TestMeta(unittest.TestCase):
    def test_progresso_e_quanto_falta(self):
        meta = Meta("Viagem", Decimal("4000.00"))
        meta.depositar(Decimal("1000.00"))
        self.assertEqual(meta.percentual, Decimal("25"))
        self.assertEqual(meta.falta, Decimal("3000.00"))
        self.assertFalse(meta.concluida)

    def test_meta_concluida_nao_passa_de_100_por_cento(self):
        meta = Meta("Celular novo", Decimal("1500.00"))
        meta.depositar(Decimal("1600.00"))
        self.assertTrue(meta.concluida)
        self.assertEqual(meta.percentual, Decimal("100"))
        self.assertEqual(meta.falta, Decimal("0"))

    def test_recusa_valores_invalidos(self):
        with self.assertRaises(ValueError):
            Meta("Viagem", Decimal("0"))
        with self.assertRaises(ValueError):
            Meta("   ", Decimal("100"))
        with self.assertRaises(ValueError):
            Meta("Viagem", Decimal("100")).depositar(Decimal("-5"))


class TestMetasNaCarteira(unittest.TestCase):
    def setUp(self):
        self.carteira = Carteira()
        self.carteira.criar_meta("Reserva de emergência", Decimal("10000.00"))

    def test_deposita_sem_diferenciar_maiusculas(self):
        self.carteira.depositar_na_meta("reserva de EMERGÊNCIA", Decimal("1500.00"))
        self.assertEqual(self.carteira.metas()[0].valor_guardado, Decimal("1500.00"))

    def test_nao_permite_meta_com_nome_repetido(self):
        with self.assertRaisesRegex(ValueError, "já existe"):
            self.carteira.criar_meta("Reserva de Emergência", Decimal("5000.00"))

    def test_deposito_em_meta_inexistente(self):
        with self.assertRaisesRegex(ValueError, "não encontrada"):
            self.carteira.depositar_na_meta("Carro", Decimal("100.00"))


class TestPersistenciaDasMetas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = Path(self.pasta.name) / "dados.json"

    def tearDown(self):
        self.pasta.cleanup()

    def test_metas_sao_salvas_e_carregadas(self):
        carteira = Carteira()
        carteira.criar_meta("Viagem", Decimal("4000.00"))
        carteira.depositar_na_meta("Viagem", Decimal("250.00"))
        armazenamento.salvar(carteira, self.arquivo)
        self.assertEqual(armazenamento.carregar(self.arquivo).metas(), carteira.metas())

    def test_arquivo_criado_antes_das_metas_continua_funcionando(self):
        antigo = {"versao_formato": 1, "lancamentos": []}
        self.arquivo.write_text(json.dumps(antigo), encoding="utf-8")
        self.assertEqual(armazenamento.carregar(self.arquivo).metas(), [])


class TestFormatacaoDoProgresso(unittest.TestCase):
    def test_percentual_com_uma_casa(self):
        self.assertEqual(formatar_percentual(Decimal("15")), "15,0%")

    def test_barra(self):
        self.assertEqual(barra_de_progresso(Decimal("25"), tamanho=8), "[##------]")


if __name__ == "__main__":
    unittest.main()
