"""Conversão e formatação de valores e datas no padrão brasileiro."""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

CENTAVOS = Decimal("0.01")


def ler_valor(texto: str) -> Decimal:
    """Converte o valor digitado pela pessoa em Decimal com duas casas.

    Aceita vírgula ou ponto como separador decimal. Quando há vírgula, o ponto é
    tratado como separador de milhar. Exemplos válidos: "45,90", "45.90",
    "1.234,56", "R$ 1.234,56" e "1500".
    """
    limpo = texto.strip().replace("R$", "").replace(" ", "")
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        valor = Decimal(limpo)
    except InvalidOperation:
        raise ValueError(f"valor inválido: {texto!r} (exemplos: 45,90 ou 1.234,56)") from None
    if not valor.is_finite():
        raise ValueError(f"valor inválido: {texto!r} (exemplos: 45,90 ou 1.234,56)")
    if valor.as_tuple().exponent < -2:
        raise ValueError(f"valor inválido: {texto!r} (use no máximo duas casas decimais)")
    return valor.quantize(CENTAVOS)


def formatar_moeda(valor: Decimal) -> str:
    """Formata um valor em reais: Decimal("1234.5") -> "R$ 1.234,50"."""
    numero = f"{abs(valor):,.2f}".translate(str.maketrans(",.", ".,"))
    sinal = "-" if valor < 0 else ""
    return f"{sinal}R$ {numero}"


def formatar_data(dia: date) -> str:
    """Formata uma data como DD/MM/AAAA."""
    return dia.strftime("%d/%m/%Y")


def formatar_percentual(valor: Decimal) -> str:
    """Formata um percentual com uma casa decimal: Decimal("15") -> "15,0%"."""
    return f"{valor:.1f}".replace(".", ",") + "%"


def barra_de_progresso(percentual: Decimal, tamanho: int = 20) -> str:
    """Desenha uma barra de progresso em texto: [#####---------------]."""
    cheios = int(percentual * tamanho / 100)
    return "[" + "#" * cheios + "-" * (tamanho - cheios) + "]"
