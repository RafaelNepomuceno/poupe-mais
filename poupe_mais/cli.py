"""Interface de linha de comando do Poupe+."""

from __future__ import annotations

import argparse

from poupe_mais import __version__


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
    return parser


def main(argv: list[str] | None = None) -> int:
    """Executa o Poupe+ e devolve o código de saída do programa."""
    parser = criar_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0
