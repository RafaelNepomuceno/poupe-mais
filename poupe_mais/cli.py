"""Interface de linha de comando do Poupe+."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime

from poupe_mais import __version__, armazenamento
from poupe_mais.carteira import CATEGORIA_PADRAO, Carteira
from poupe_mais.formatacao import formatar_data, formatar_moeda, ler_valor
from poupe_mais.modelos import TipoLancamento
from poupe_mais.relatorios import formatar_resumo, gerar_resumo

ARQUIVO_PADRAO = "poupe_dados.json"


def ler_data(texto: str) -> date:
    """Converte DD/MM/AAAA (ou AAAA-MM-DD) em data."""
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            pass
    raise argparse.ArgumentTypeError(f"data inválida: {texto!r} (use DD/MM/AAAA)")


def ler_mes(texto: str) -> tuple[int, int]:
    """Converte MM/AAAA (ou AAAA-MM) em (ano, mês)."""
    for formato in ("%m/%Y", "%Y-%m"):
        try:
            referencia = datetime.strptime(texto, formato)
            return referencia.year, referencia.month
        except ValueError:
            pass
    raise argparse.ArgumentTypeError(f"mês inválido: {texto!r} (use MM/AAAA)")


def _registrar(args: argparse.Namespace, carteira: Carteira) -> None:
    tipo = TipoLancamento(args.comando)
    lancamento = carteira.registrar(
        tipo=tipo,
        valor=ler_valor(args.valor),
        descricao=args.descricao,
        categoria=args.categoria,
        data=args.data,
    )
    print(
        f"{tipo.value.capitalize()} registrada (#{lancamento.id}): {lancamento.descricao} — "
        f"{formatar_moeda(lancamento.valor)} em {formatar_data(lancamento.data)} "
        f"[{lancamento.categoria}]"
    )


def _listar(args: argparse.Namespace, carteira: Carteira) -> None:
    ano, mes = args.mes if args.mes else (None, None)
    lancamentos = carteira.lancamentos(ano=ano, mes=mes)
    if not lancamentos:
        print("Nenhum lançamento encontrado.")
        return
    cabecalho = ("#", "Data", "Tipo", "Categoria", "Descrição", "Valor")
    linhas = [
        (
            str(item.id),
            formatar_data(item.data),
            item.tipo.value,
            item.categoria,
            item.descricao,
            formatar_moeda(item.valor_com_sinal),
        )
        for item in lancamentos
    ]
    print(_tabela(cabecalho, linhas, alinhar_a_direita={0, 5}))


def _saldo(args: argparse.Namespace, carteira: Carteira) -> None:
    print(f"Saldo atual: {formatar_moeda(carteira.saldo())}")


def _resumo(args: argparse.Namespace, carteira: Carteira) -> None:
    hoje = date.today()
    ano, mes = args.mes if args.mes else (hoje.year, hoje.month)
    print(formatar_resumo(gerar_resumo(carteira, ano, mes)))


def _tabela(cabecalho, linhas, alinhar_a_direita=frozenset()) -> str:
    larguras = [max(len(celula) for celula in coluna) for coluna in zip(cabecalho, *linhas)]

    def montar(celulas) -> str:
        partes = [
            celula.rjust(largura) if indice in alinhar_a_direita else celula.ljust(largura)
            for indice, (celula, largura) in enumerate(zip(celulas, larguras))
        ]
        return "  ".join(partes).rstrip()

    return "\n".join(montar(celulas) for celulas in [cabecalho, *linhas])


def criar_parser() -> argparse.ArgumentParser:
    """Monta o analisador de argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        prog="poupe",
        description="Poupe+ — controle financeiro pessoal pela linha de comando.",
    )
    parser.add_argument(
        "--versao",
        action="version",
        version=f"Poupe+ {__version__}",
        help="mostra a versão do sistema e sai",
    )
    parser.add_argument(
        "--arquivo",
        default=os.environ.get("POUPE_ARQUIVO", ARQUIVO_PADRAO),
        help="arquivo onde os dados ficam guardados (padrão: %(default)s)",
    )
    comandos = parser.add_subparsers(dest="comando", title="comandos", metavar="<comando>")

    for tipo in TipoLancamento:
        registrar = comandos.add_parser(tipo.value, help=f"registra uma {tipo.value}")
        registrar.add_argument("valor", help="valor em reais, ex.: 45,90 ou 1.234,56")
        registrar.add_argument("descricao", help='descrição, ex.: "Conta de luz"')
        registrar.add_argument(
            "-c", "--categoria", default=CATEGORIA_PADRAO, help="categoria (padrão: %(default)s)"
        )
        registrar.add_argument(
            "-d", "--data", type=ler_data, help="data no formato DD/MM/AAAA (padrão: hoje)"
        )
        registrar.set_defaults(funcao=_registrar, altera_dados=True)

    listar = comandos.add_parser("listar", help="lista os lançamentos")
    listar.add_argument("-m", "--mes", type=ler_mes, help="mostra só um mês, no formato MM/AAAA")
    listar.set_defaults(funcao=_listar, altera_dados=False)

    saldo = comandos.add_parser("saldo", help="mostra o saldo atual")
    saldo.set_defaults(funcao=_saldo, altera_dados=False)

    resumo = comandos.add_parser("resumo", help="mostra o resumo do mês por categoria")
    resumo.add_argument("-m", "--mes", type=ler_mes, help="mês no formato MM/AAAA (padrão: mês atual)")
    resumo.set_defaults(funcao=_resumo, altera_dados=False)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Executa o Poupe+ e devolve o código de saída do programa."""
    parser = criar_parser()
    args = parser.parse_args(argv)
    if args.comando is None:
        parser.print_help()
        return 0

    carteira = armazenamento.carregar(args.arquivo)
    try:
        args.funcao(args, carteira)
    except ValueError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    if args.altera_dados:
        armazenamento.salvar(carteira, args.arquivo)
    return 0
