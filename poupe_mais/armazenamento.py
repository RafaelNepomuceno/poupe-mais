"""Leitura e gravação dos dados do Poupe+ em um arquivo JSON."""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from poupe_mais.carteira import Carteira
from poupe_mais.modelos import Lancamento, Meta, TipoLancamento

# Versão do formato do arquivo. Deve mudar se a estrutura do JSON mudar.
VERSAO_FORMATO = 1


def carregar(caminho: str | Path) -> Carteira:
    """Lê a carteira do arquivo. Se o arquivo não existir, começa vazia."""
    caminho = Path(caminho)
    if not caminho.exists():
        return Carteira()
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    lancamentos = [_lancamento_de_dict(item) for item in dados.get("lancamentos", [])]
    # Arquivos criados antes das metas existirem não têm a chave "metas".
    metas = [_meta_de_dict(item) for item in dados.get("metas", [])]
    return Carteira(lancamentos, metas)


def salvar(carteira: Carteira, caminho: str | Path) -> None:
    """Grava a carteira no arquivo (primeiro em um temporário, para não corromper)."""
    caminho = Path(caminho)
    dados = {
        "versao_formato": VERSAO_FORMATO,
        "lancamentos": [_lancamento_para_dict(item) for item in carteira.lancamentos()],
        "metas": [_meta_para_dict(item) for item in carteira.metas()],
    }
    temporario = caminho.with_name(caminho.name + ".tmp")
    temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporario.replace(caminho)


def _lancamento_para_dict(lancamento: Lancamento) -> dict:
    return {
        "id": lancamento.id,
        "tipo": lancamento.tipo.value,
        "valor": str(lancamento.valor),
        "descricao": lancamento.descricao,
        "categoria": lancamento.categoria,
        "data": lancamento.data.isoformat(),
    }


def _lancamento_de_dict(dados: dict) -> Lancamento:
    return Lancamento(
        id=int(dados["id"]),
        tipo=TipoLancamento(dados["tipo"]),
        valor=Decimal(dados["valor"]),
        descricao=dados["descricao"],
        categoria=dados["categoria"],
        data=date.fromisoformat(dados["data"]),
    )


def _meta_para_dict(meta: Meta) -> dict:
    return {
        "nome": meta.nome,
        "valor_alvo": str(meta.valor_alvo),
        "valor_guardado": str(meta.valor_guardado),
    }


def _meta_de_dict(dados: dict) -> Meta:
    return Meta(
        nome=dados["nome"],
        valor_alvo=Decimal(dados["valor_alvo"]),
        valor_guardado=Decimal(dados["valor_guardado"]),
    )
