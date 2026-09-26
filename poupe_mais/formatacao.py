"""Formatação de valores e datas no padrão brasileiro."""

from __future__ import annotations

from datetime import date
from decimal import Decimal


def formatar_moeda(valor: Decimal) -> str:
    """Formata um valor em reais: Decimal("1234.5") -> "R$ 1.234,50"."""
    numero = f"{abs(valor):,.2f}".translate(str.maketrans(",.", ".,"))
    sinal = "-" if valor < 0 else ""
    return f"{sinal}R$ {numero}"


def formatar_data(dia: date) -> str:
    """Formata uma data como DD/MM/AAAA."""
    return dia.strftime("%d/%m/%Y")
