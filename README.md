# Poupe+

> Controle financeiro pessoal pela linha de comando.

O **Poupe+** é um sistema simples de controle financeiro pessoal. Ele registra
receitas e despesas, mostra o saldo e ajuda a entender para onde o dinheiro vai
a cada mês — o primeiro passo para conseguir poupar.

> Projeto em desenvolvimento. O andamento pode ser acompanhado pelo histórico
> de commits.

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

# consultar
python -m poupe_mais listar --mes 09/2026
python -m poupe_mais saldo
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
│   ├── modelos.py       entidades do domínio (Lancamento)
│   ├── carteira.py      regras de negócio: lançamentos e saldo
│   ├── armazenamento.py leitura e gravação dos dados em JSON
│   └── formatacao.py    formatação de valores e datas no padrão brasileiro
├── tests/               testes automatizados
├── pyproject.toml       configuração e metadados do projeto
└── README.md
```

## Autor

Rafael Nepomuceno — Bacharelado em Sistemas de Informação (UFRPE), disciplina
Fundamentos de Engenharia de Software.
