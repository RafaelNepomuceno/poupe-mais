import unittest
from datetime import date
from decimal import Decimal

from poupe_mais.carteira import Carteira, normalizar_categoria
from poupe_mais.modelos import TipoLancamento

RECEITA = TipoLancamento.RECEITA
DESPESA = TipoLancamento.DESPESA


class TestCarteira(unittest.TestCase):
    def setUp(self):
        self.carteira = Carteira()

    def test_registra_receita_e_despesa_e_calcula_saldo(self):
        self.carteira.registrar(RECEITA, Decimal("3000.00"), "Salário", "Salário", date(2026, 9, 5))
        self.carteira.registrar(DESPESA, Decimal("1200.50"), "Aluguel", "Moradia", date(2026, 9, 10))
        self.assertEqual(self.carteira.saldo(), Decimal("1799.50"))

    def test_ids_sao_sequenciais(self):
        primeiro = self.carteira.registrar(RECEITA, Decimal("10"), "Pix recebido")
        segundo = self.carteira.registrar(DESPESA, Decimal("5"), "Café")
        self.assertEqual((primeiro.id, segundo.id), (1, 2))

    def test_recusa_valor_zero_ou_negativo(self):
        for valor in ("0", "-10"):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                self.carteira.registrar(DESPESA, Decimal(valor), "Teste")

    def test_recusa_descricao_vazia(self):
        with self.assertRaises(ValueError):
            self.carteira.registrar(DESPESA, Decimal("10"), "   ")

    def test_filtra_lancamentos_por_mes(self):
        self.carteira.registrar(DESPESA, Decimal("10"), "Agosto", data=date(2026, 8, 31))
        self.carteira.registrar(DESPESA, Decimal("20"), "Setembro", data=date(2026, 9, 1))
        setembro = self.carteira.lancamentos(ano=2026, mes=9)
        self.assertEqual([item.descricao for item in setembro], ["Setembro"])

    def test_lista_em_ordem_de_data(self):
        self.carteira.registrar(DESPESA, Decimal("10"), "Depois", data=date(2026, 9, 20))
        self.carteira.registrar(DESPESA, Decimal("10"), "Antes", data=date(2026, 9, 2))
        descricoes = [item.descricao for item in self.carteira.lancamentos()]
        self.assertEqual(descricoes, ["Antes", "Depois"])

    def test_sem_data_usa_o_dia_de_hoje(self):
        lancamento = self.carteira.registrar(RECEITA, Decimal("10"), "Pix recebido")
        self.assertEqual(lancamento.data, date.today())


class TestNormalizarCategoria(unittest.TestCase):
    def test_padroniza_o_nome(self):
        self.assertEqual(normalizar_categoria("  alimentação "), "Alimentação")

    def test_categoria_vazia_vira_outros(self):
        self.assertEqual(normalizar_categoria(""), "Outros")


if __name__ == "__main__":
    unittest.main()
