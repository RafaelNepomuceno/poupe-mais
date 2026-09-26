"""Regras de negócio: registro de lançamentos e cálculo do saldo."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from poupe_mais.modelos import Lancamento, Meta, TipoLancamento

CATEGORIA_PADRAO = "Outros"


def normalizar_categoria(categoria: str) -> str:
    """Padroniza o nome da categoria ("alimentação" -> "Alimentação")."""
    categoria = " ".join(categoria.split())
    if not categoria:
        return CATEGORIA_PADRAO
    return categoria[0].upper() + categoria[1:]


class Carteira:
    """Guarda os lançamentos e as metas de uma pessoa e calcula o saldo."""

    def __init__(
        self,
        lancamentos: list[Lancamento] | None = None,
        metas: list[Meta] | None = None,
    ) -> None:
        self._lancamentos: list[Lancamento] = list(lancamentos or [])
        self._metas: list[Meta] = list(metas or [])

    def registrar(
        self,
        tipo: TipoLancamento,
        valor: Decimal,
        descricao: str,
        categoria: str = CATEGORIA_PADRAO,
        data: date | None = None,
    ) -> Lancamento:
        """Registra uma receita ou despesa e devolve o lançamento criado."""
        lancamento = Lancamento(
            id=self._proximo_id(),
            tipo=tipo,
            valor=valor,
            descricao=descricao.strip(),
            categoria=normalizar_categoria(categoria),
            data=data or date.today(),
        )
        self._lancamentos.append(lancamento)
        return lancamento

    def lancamentos(self, ano: int | None = None, mes: int | None = None) -> list[Lancamento]:
        """Lista os lançamentos em ordem de data, opcionalmente filtrando por mês."""
        selecionados = [
            lancamento
            for lancamento in self._lancamentos
            if (ano is None or lancamento.data.year == ano)
            and (mes is None or lancamento.data.month == mes)
        ]
        return sorted(selecionados, key=lambda lancamento: (lancamento.data, lancamento.id))

    def saldo(self) -> Decimal:
        """Soma das receitas menos a soma das despesas."""
        return sum((lancamento.valor_com_sinal for lancamento in self._lancamentos), Decimal("0.00"))

    def criar_meta(self, nome: str, valor_alvo: Decimal) -> Meta:
        """Cria uma meta de economia. O nome não pode se repetir."""
        nome = " ".join(nome.split())
        if self._buscar_meta(nome) is not None:
            raise ValueError(f"já existe uma meta chamada {nome!r}")
        meta = Meta(nome, valor_alvo)
        self._metas.append(meta)
        return meta

    def depositar_na_meta(self, nome: str, valor: Decimal) -> Meta:
        """Registra um valor guardado para a meta informada."""
        meta = self._buscar_meta(nome)
        if meta is None:
            raise ValueError(f"meta não encontrada: {nome!r}")
        meta.depositar(valor)
        return meta

    def metas(self) -> list[Meta]:
        return list(self._metas)

    def _buscar_meta(self, nome: str) -> Meta | None:
        chave = " ".join(nome.split()).casefold()
        return next((meta for meta in self._metas if meta.nome.casefold() == chave), None)

    def _proximo_id(self) -> int:
        return max((lancamento.id for lancamento in self._lancamentos), default=0) + 1
