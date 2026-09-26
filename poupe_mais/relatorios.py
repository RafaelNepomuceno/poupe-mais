"""Relatórios do Poupe+: resumo financeiro de um mês."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from poupe_mais.carteira import Carteira
from poupe_mais.formatacao import formatar_moeda
from poupe_mais.modelos import TipoLancamento


@dataclass(frozen=True)
class ResumoMensal:
    """Totais de um mês e quanto foi gasto em cada categoria."""

    ano: int
    mes: int
    total_receitas: Decimal
    total_despesas: Decimal
    despesas_por_categoria: tuple[tuple[str, Decimal], ...]  # maior gasto primeiro

    @property
    def saldo(self) -> Decimal:
        return self.total_receitas - self.total_despesas


def gerar_resumo(carteira: Carteira, ano: int, mes: int) -> ResumoMensal:
    """Calcula o resumo do mês a partir dos lançamentos da carteira."""
    receitas = Decimal("0.00")
    despesas = Decimal("0.00")
    por_categoria: dict[str, Decimal] = defaultdict(Decimal)
    for lancamento in carteira.lancamentos(ano=ano, mes=mes):
        if lancamento.tipo is TipoLancamento.RECEITA:
            receitas += lancamento.valor
        else:
            despesas += lancamento.valor
            por_categoria[lancamento.categoria] += lancamento.valor

    categorias = sorted(por_categoria.items(), key=lambda item: (-item[1], item[0]))
    return ResumoMensal(ano, mes, receitas, despesas, tuple(categorias))


def formatar_resumo(resumo: ResumoMensal) -> str:
    """Monta o texto do resumo mensal para exibir no terminal."""
    linhas = [
        f"Resumo de {resumo.mes:02d}/{resumo.ano}",
        "",
        f"  Receitas  {formatar_moeda(resumo.total_receitas):>14}",
        f"  Despesas  {formatar_moeda(resumo.total_despesas):>14}",
        f"  Saldo     {formatar_moeda(resumo.saldo):>14}",
        "",
    ]
    if not resumo.despesas_por_categoria:
        linhas.append("Nenhuma despesa registrada no mês.")
        return "\n".join(linhas)

    largura = max(len(nome) for nome, _ in resumo.despesas_por_categoria)
    linhas.append("Despesas por categoria")
    for nome, valor in resumo.despesas_por_categoria:
        linhas.append(f"  {nome:<{largura}}  {formatar_moeda(valor):>14}")
    return "\n".join(linhas)
