"""Entidades do domínio do Poupe+."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class TipoLancamento(Enum):
    """Indica se o dinheiro entrou (receita) ou saiu (despesa)."""

    RECEITA = "receita"
    DESPESA = "despesa"


@dataclass(frozen=True)
class Lancamento:
    """Uma entrada ou saída de dinheiro registrada pela pessoa."""

    id: int
    tipo: TipoLancamento
    valor: Decimal
    descricao: str
    categoria: str
    data: date

    def __post_init__(self) -> None:
        if self.valor <= 0:
            raise ValueError("o valor deve ser maior que zero")
        if not self.descricao.strip():
            raise ValueError("a descrição não pode ficar vazia")

    @property
    def valor_com_sinal(self) -> Decimal:
        """Valor positivo para receitas e negativo para despesas."""
        if self.tipo is TipoLancamento.RECEITA:
            return self.valor
        return -self.valor
