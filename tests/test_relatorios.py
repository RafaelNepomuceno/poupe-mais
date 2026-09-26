import unittest
from datetime import date
from decimal import Decimal

from poupe_mais.carteira import Carteira
from poupe_mais.modelos import TipoLancamento
from poupe_mais.relatorios import formatar_resumo, gerar_resumo

RECEITA = TipoLancamento.RECEITA
DESPESA = TipoLancamento.DESPESA


def carteira_de_exemplo() -> Carteira:
    carteira = Carteira()
    carteira.registrar(RECEITA, Decimal("4000.00"), "Salário", "Salário", date(2026, 9, 5))
    carteira.registrar(DESPESA, Decimal("1500.00"), "Aluguel", "Moradia", date(2026, 9, 10))
    carteira.registrar(DESPESA, Decimal("600.00"), "Supermercado", "Alimentação", date(2026, 9, 12))
    carteira.registrar(DESPESA, Decimal("400.00"), "Feira e padaria", "Alimentação", date(2026, 9, 20))
    carteira.registrar(DESPESA, Decimal("500.00"), "Combustível", "Transporte", date(2026, 9, 15))
    carteira.registrar(DESPESA, Decimal("999.00"), "Mês passado", "Lazer", date(2026, 8, 30))
    return carteira


class TestGerarResumo(unittest.TestCase):
    def setUp(self):
        self.resumo = gerar_resumo(carteira_de_exemplo(), 2026, 9)

    def test_totais_do_mes(self):
        self.assertEqual(self.resumo.total_receitas, Decimal("4000.00"))
        self.assertEqual(self.resumo.total_despesas, Decimal("3000.00"))
        self.assertEqual(self.resumo.saldo, Decimal("1000.00"))

    def test_categorias_do_maior_para_o_menor_gasto(self):
        self.assertEqual(
            self.resumo.despesas_por_categoria,
            (
                ("Moradia", Decimal("1500.00")),
                ("Alimentação", Decimal("1000.00")),
                ("Transporte", Decimal("500.00")),
            ),
        )

    def test_mes_sem_lancamentos(self):
        resumo = gerar_resumo(carteira_de_exemplo(), 2026, 10)
        self.assertEqual(resumo.total_receitas, Decimal("0"))
        self.assertEqual(resumo.total_despesas, Decimal("0"))
        self.assertEqual(resumo.despesas_por_categoria, ())


class TestFormatarResumo(unittest.TestCase):
    def test_texto_do_resumo(self):
        texto = formatar_resumo(gerar_resumo(carteira_de_exemplo(), 2026, 9))
        self.assertEqual(
            texto.splitlines(),
            [
                "Resumo de 09/2026",
                "",
                "  Receitas     R$ 4.000,00",
                "  Despesas     R$ 3.000,00",
                "  Saldo        R$ 1.000,00",
                "",
                "Despesas por categoria",
                "  Moradia         R$ 1.500,00",
                "  Alimentação     R$ 1.000,00",
                "  Transporte        R$ 500,00",
            ],
        )

    def test_mes_sem_despesas(self):
        texto = formatar_resumo(gerar_resumo(Carteira(), 2026, 9))
        self.assertIn("Nenhuma despesa registrada no mês.", texto)


if __name__ == "__main__":
    unittest.main()
