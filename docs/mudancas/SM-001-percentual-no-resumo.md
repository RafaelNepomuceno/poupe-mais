# SM-001 — Percentual por categoria e taxa de poupança no resumo mensal

| Campo                  | Registro                                  |
|------------------------|-------------------------------------------|
| Data da solicitação    | 26/09/2026                                |
| Solicitante            | Rafael Nepomuceno                         |
| Versão de referência   | v1.0.0                                    |
| Funcionalidade afetada | Resumo mensal (comando `resumo`)          |
| Tipo de mudança        | Melhoria (evolutiva)                      |
| Situação               | Concluída — liberada na versão 1.1.0      |

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

Implementada na branch `feature/sm-001-percentual-resumo`, integrada à `main`
por merge e liberada na versão 1.1.0 (tag `v1.1.0`).

O que foi feito:

- `ResumoMensal` ganhou a propriedade `taxa_de_poupanca` e o método
  `percentual_das_despesas`;
- `formatar_resumo` passou a exibir a taxa de poupança e o percentual de cada
  categoria;
- foram criados 4 testes: taxa de poupança, percentuais, mês sem receitas e mês
  em que se gastou mais do que se ganhou (taxa negativa).

Arquivos alterados: `poupe_mais/relatorios.py`, `tests/test_relatorios.py`,
`README.md` e este documento — os mesmos previstos na análise de impacto.
`cli.py` não precisou ser alterado.

Problemas encontrados:

- Ao rodar os testes existentes logo após alterar o código, 1 dos 40 testes
  falhou: `test_texto_do_resumo`, que conferia o texto exato do resumo da
  v1.0.0. A falha era esperada (estava prevista na análise de impacto), porque
  o formato do resumo mudou de propósito. O teste foi atualizado para o novo
  formato.
- Os outros 39 testes passaram sem nenhuma alteração, o que indica que
  cadastro, metas e armazenamento não foram afetados.
- Um arquivo de dados criado com a v1.0.0 foi lido normalmente pela nova
  versão, já que o formato do JSON não mudou.

Situação final: 44 testes, todos passando.
