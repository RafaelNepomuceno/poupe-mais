# Poupe+

> Controle financeiro pessoal pela linha de comando.

O **Poupe+** é um sistema simples de controle financeiro pessoal. Ele registra
receitas e despesas, mostra o saldo e ajuda a entender para onde o dinheiro vai
a cada mês — o primeiro passo para conseguir poupar.

## Objetivo

Oferecer uma ferramenta leve, sem dependências externas, para que uma pessoa
registre o dinheiro que entra e sai no dia a dia, acompanhe o saldo, analise os
gastos de cada mês e acompanhe suas metas de economia.

## Principais funcionalidades

- Cadastro de receitas e despesas, com valor, descrição, categoria e data
- Consulta dos lançamentos e do saldo atual
- Resumo mensal com receitas, despesas e gastos por categoria
- Metas de economia com acompanhamento do progresso

## Como executar

Requisito: Python 3.10 ou superior. Não há dependências externas.

```bash
python -m poupe_mais --help
```

Os dados ficam no arquivo `poupe_dados.json`, na pasta onde o comando é
executado. Para usar outro arquivo, informe `--arquivo caminho.json` ou defina a
variável de ambiente `POUPE_ARQUIVO`.

## Como usar

```bash
# registrar receitas e despesas (categoria e data são opcionais)
python -m poupe_mais receita 4800 "Salário de setembro" -c Salário -d 05/09/2026
python -m poupe_mais despesa 1300 "Aluguel" -c Moradia -d 10/09/2026
python -m poupe_mais despesa 45,90 "Almoço" -c Alimentação   # vírgula ou ponto

# consultar
python -m poupe_mais listar --mes 09/2026
python -m poupe_mais saldo

# resumo do mês: receitas, despesas, saldo e gastos por categoria
python -m poupe_mais resumo --mes 09/2026

# metas de economia
python -m poupe_mais meta criar "Reserva de emergência" 10.000,00
python -m poupe_mais meta depositar "Reserva de emergência" 1.500,00
python -m poupe_mais meta listar
```

Exemplo de resumo mensal, com o peso de cada categoria nas despesas e a taxa
de poupança (quanto da receita sobrou):

```text
$ python -m poupe_mais resumo --mes 09/2026
Resumo de 09/2026

  Receitas     R$ 5.450,00
  Despesas     R$ 3.277,75
  Saldo        R$ 2.172,25
  Taxa de poupança: 39,9%

Despesas por categoria
  Moradia         R$ 1.650,00   50,3%
  Alimentação       R$ 922,80   28,2%
  Transporte        R$ 298,70    9,1%
  Contas            R$ 286,25    8,7%
  Lazer             R$ 120,00    3,7%
```

## Como rodar os testes

```bash
python -m unittest
```

## Estrutura do projeto

```text
poupe-mais/
├── poupe_mais/          código-fonte do sistema
│   ├── __init__.py      versão do sistema
│   ├── __main__.py      ponto de entrada (python -m poupe_mais)
│   ├── cli.py           interface de linha de comando
│   ├── modelos.py       entidades do domínio (Lancamento e Meta)
│   ├── carteira.py      regras de negócio: lançamentos, saldo e metas
│   ├── armazenamento.py leitura e gravação dos dados em JSON
│   ├── relatorios.py    resumo mensal por categoria
│   └── formatacao.py    formatação de valores e datas no padrão brasileiro
├── tests/               testes automatizados
├── CHANGELOG.md         histórico das versões
├── pyproject.toml       configuração e metadados do projeto
└── README.md
```

## Versões

O projeto segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/)
(MAJOR.MINOR.PATCH). Cada versão publicada é marcada com uma tag no Git
(ex.: `v1.0.0`) e descrita no [CHANGELOG](CHANGELOG.md). As mensagens de
commit seguem o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/)
(`feat`, `fix`, `docs`, `chore`...).

## Autor

Rafael Nepomuceno — Bacharelado em Sistemas de Informação (UFRPE), disciplina
Fundamentos de Engenharia de Software.
