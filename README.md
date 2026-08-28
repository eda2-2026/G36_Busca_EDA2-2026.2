# G36_Busca_EDA2-2026.2 — EstoqueHash

Sistema de linha de comando (CLI) em Python para **controle de estoque**, com busca de
produtos por **código de barras** usando uma **tabela hash**.

O objetivo do trabalho é implementar a busca por hashing e **comparar seu desempenho com a
busca sequencial** conforme a base de produtos cresce.

## Alunos

| Matrícula   | Nome                            |
| ----------- | ------------------------------- |
| 231011328   | Felipe de Aquino Campelo        |
| 232000688 | Arthur Palhares Ferreira Silva  |

## Descrição

O sistema gerencia um catálogo de produtos (código de barras, nome, quantidade, preço) e
permite cadastrar, buscar, atualizar estoque (entrada/saída), remover e listar produtos,
além de emitir alerta de estoque baixo. Os dados são persistidos em arquivo CSV.

Cada busca informa o **número de comparações** realizadas, permitindo o experimento
comparativo entre os dois algoritmos.

## Algoritmos de busca

- **Tabela hash (endereçamento aberto com sondagem linear)** — busca principal, por código
  de barras. Função hash própria e redimensionamento automático quando o fator de carga
  fica alto.
- **Busca sequencial** — sobre os mesmos dados, apenas para servir de base de comparação
  (tempo de execução e número de comparações).

## Como executar

Requisitos: Python 3.11+.

```bash
pip install -r requirements.txt      # pytest
python main.py                       # abre o menu do CLI
```

Testes automatizados:

```bash
pytest
```

Experimento de desempenho (hash × sequencial):

```bash
python benchmark.py
```

## Estrutura do projeto

```
main.py              CLI (menu)
tabela_hash.py       tabela hash com sondagem linear
busca_sequencial.py  busca linear com contador de comparações
estoque.py           regras de negócio + leitura/escrita do CSV
benchmark.py         experimento hash x sequencial
test_estoque.py      testes automatizados
```
