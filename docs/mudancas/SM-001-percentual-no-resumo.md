# SM-001 — Percentual por categoria e taxa de poupança no resumo mensal

| Campo                  | Registro                                  |
|------------------------|-------------------------------------------|
| Data da solicitação    | 26/09/2026                                |
| Solicitante            | Rafael Nepomuceno                         |
| Versão de referência   | v1.0.0                                    |
| Funcionalidade afetada | Resumo mensal (comando `resumo`)          |
| Tipo de mudança        | Melhoria (evolutiva)                      |
| Situação               | Aprovada — aguardando implementação       |

## O que será modificado

O resumo mensal passará a mostrar:

1. ao lado de cada categoria de despesa, o percentual que ela representa no
   total de despesas do mês;
2. a taxa de poupança do mês, isto é, quanto da receita sobrou
   (saldo ÷ receitas × 100).

## Motivo

Na versão 1.0.0 o resumo mostra apenas valores absolutos. Com eles não é
imediato perceber o peso de cada gasto: saber que a moradia custou
R$ 1.650,00 diz menos do que saber que ela representa metade das despesas do
mês. A taxa de poupança, por sua vez, responde diretamente à pergunta que
motivou o sistema: "quanto eu consegui poupar neste mês?".

## Análise de impacto

Arquivos que serão alterados na implementação:

| Arquivo                                        | Alteração prevista                                                     |
|------------------------------------------------|------------------------------------------------------------------------|
| `poupe_mais/relatorios.py`                     | calcular os percentuais e a taxa de poupança e exibi-los no resumo     |
| `tests/test_relatorios.py`                     | novos testes; o teste que confere o texto do resumo vai quebrar e precisará ser atualizado |
| `README.md`                                    | incluir um exemplo da saída do comando `resumo`                        |
| `docs/mudancas/SM-001-percentual-no-resumo.md` | registrar o resultado da mudança                                       |

Na liberação da versão também mudam `CHANGELOG.md` e `poupe_mais/__init__.py`
(número da versão).

Não devem ser afetados: a interface de linha de comando (`cli.py`), o formato
do arquivo de dados (`poupe_dados.json`), o cadastro de lançamentos e as metas.
A mudança é compatível com a versão anterior e, pelo Versionamento Semântico,
gera a versão **1.1.0**.

## Critérios de aceitação

- Cada categoria mostra seu percentual com uma casa decimal (ex.: 50,3%).
- A taxa de poupança aparece junto aos totais; em mês sem receitas ela não é
  calculada e o resumo não pode falhar.
- Todos os testes automatizados passam.

## Resultado

_A preencher após a implementação._
