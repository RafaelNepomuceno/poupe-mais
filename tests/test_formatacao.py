import unittest
from datetime import date
from decimal import Decimal

from poupe_mais.formatacao import formatar_data, formatar_moeda, ler_valor


class TestLerValor(unittest.TestCase):
    def test_aceita_formatos_usados_no_brasil(self):
        casos = {
            "45,90": "45.90",
            "45.90": "45.90",
            "1.234,56": "1234.56",
            "R$ 1.234,56": "1234.56",
            "1500": "1500.00",
            "0,5": "0.50",
        }
        for texto, esperado in casos.items():
            with self.subTest(texto=texto):
                self.assertEqual(ler_valor(texto), Decimal(esperado))

    def test_recusa_texto_que_nao_e_numero(self):
        for texto in ("abc", "", "12,3,4", "NaN", "Infinity"):
            with self.subTest(texto=texto), self.assertRaises(ValueError):
                ler_valor(texto)

    def test_recusa_mais_de_duas_casas_decimais(self):
        with self.assertRaisesRegex(ValueError, "duas casas decimais"):
            ler_valor("10,999")


class TestFormatar(unittest.TestCase):
    def test_moeda(self):
        self.assertEqual(formatar_moeda(Decimal("1234.5")), "R$ 1.234,50")
        self.assertEqual(formatar_moeda(Decimal("-45.9")), "-R$ 45,90")
        self.assertEqual(formatar_moeda(Decimal("1000000")), "R$ 1.000.000,00")

    def test_data(self):
        self.assertEqual(formatar_data(date(2026, 9, 5)), "05/09/2026")


if __name__ == "__main__":
    unittest.main()
