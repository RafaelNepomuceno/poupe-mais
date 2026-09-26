# Histórico de versões

Todas as mudanças relevantes do Poupe+ são registradas neste arquivo.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2026-09-26

### Adicionado

- O resumo mensal mostra o percentual de cada categoria no total de despesas e
  a taxa de poupança do mês (solicitação de mudança SM-001).

## [1.0.0] - 2026-09-26

Primeira versão estável.

### Adicionado

- Cadastro de receitas e despesas com valor, descrição, categoria e data.
- Listagem dos lançamentos, com filtro por mês, e consulta do saldo atual.
- Resumo mensal com receitas, despesas, saldo e gastos por categoria.
- Metas de economia com registro de depósitos e barra de progresso.

### Corrigido

- Valores digitados com vírgula (ex.: 45,90) encerravam o programa com erro;
  agora são aceitos, e valores inválidos geram uma mensagem clara.
