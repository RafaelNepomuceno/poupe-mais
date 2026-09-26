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


@dataclass
class Meta:
    """Um objetivo de economia, como uma reserva de emergência ou uma viagem."""

    nome: str
    valor_alvo: Decimal
    valor_guardado: Decimal = Decimal("0.00")

    def __post_init__(self) -> None:
        if not self.nome.strip():
            raise ValueError("o nome da meta não pode ficar vazio")
        if self.valor_alvo <= 0:
            raise ValueError("o valor da meta deve ser maior que zero")

    def depositar(self, valor: Decimal) -> None:
        """Soma um valor guardado ao que já foi juntado para a meta."""
        if valor <= 0:
            raise ValueError("o valor do depósito deve ser maior que zero")
        self.valor_guardado += valor

    @property
    def falta(self) -> Decimal:
        """Quanto ainda falta juntar (nunca negativo)."""
        return max(self.valor_alvo - self.valor_guardado, Decimal("0.00"))

    @property
    def percentual(self) -> Decimal:
        """Progresso da meta, de 0 a 100."""
        return min(self.valor_guardado * 100 / self.valor_alvo, Decimal(100))

    @property
    def concluida(self) -> bool:
        return self.valor_guardado >= self.valor_alvo
