# G36_Busca_EDA2-2026.2 - EstoqueHash

Sistema de linha de comando (CLI) em Python para controle de estoque, com busca de
produtos por codigo de barras usando uma tabela hash.

O objetivo do trabalho e aplicar os conceitos de busca estudados em EDA2, implementando
uma tabela hash e comparando seu desempenho com a busca sequencial conforme a base de
produtos cresce.

## Alunos

| Matrícula   | Nome                            |
| ----------- | ------------------------------- |
| 231011328   | Felipe de Aquino Campelo        |
| 232000688 | Arthur Palhares Ferreira Silva  |

## Descrição

O sistema gerencia um catálogo de produtos (código de barras, nome, quantidade, preço) e
permite cadastrar, buscar, atualizar estoque (entrada/saída), remover e listar produtos,
além de emitir alerta de estoque baixo. Os dados são persistidos em arquivo CSV.

Cada busca informa o número de comparações realizadas, permitindo o experimento
comparativo entre os dois algoritmos.

## Algoritmos de busca

- Tabela hash com enderecamento aberto e sondagem linear: busca principal por codigo de
  barras. A tabela usa funcao hash propria, tratamento de colisao e redimensionamento
  automatico quando o fator de carga fica alto.
- Busca sequencial: percorre a lista de produtos item por item, servindo como base de
  comparacao em tempo de execucao e quantidade de comparacoes.

## Conceitos aplicados

- chave primaria: o codigo de barras identifica cada produto;
- funcao hash: transforma a chave em um indice do vetor;
- colisao: ocorre quando duas chaves caem no mesmo indice;
- sondagem linear: em caso de colisao, o sistema procura a proxima posicao disponivel;
- fator de carga: relacao entre quantidade de elementos e capacidade da tabela;
- marcador de remocao: posicoes removidas sao marcadas para nao interromper buscas futuras.

## Como executar

Requisitos: Python 3.11+.

```bash
pip install -r requirements.txt
python main.py
```

Se o comando `python` nao estiver disponivel no ambiente, use `python3`.

O CLI tambem aceita um arquivo CSV diferente e outro limite para alerta de estoque baixo:

```bash
python main.py --dados produtos.csv --limite 5
```

Testes automatizados:

```bash
pytest
```

Experimento de desempenho (hash × sequencial):

```bash
python benchmark.py
```

Para rodar o benchmark sem gerar graficos:

```bash
python benchmark.py --sem-graficos
```

O benchmark imprime uma tabela com comparacoes medias, maximo de comparacoes e tempo medio
por busca. Quando os graficos estao habilitados, os arquivos sao salvos em `resultados/`.

Casos didaticos de melhor, medio e pior caso:

```bash
python casos.py
```

## Estrutura do projeto

```
main.py                CLI com menu interativo
tabela_hash.py         tabela hash com sondagem linear
busca_sequencial.py    busca linear com contador de comparacoes
estoque.py             produto, validacoes, regras de estoque e CSV
benchmark.py           experimento hash x sequencial
casos.py               exemplos de melhor, medio e pior caso
produtos.csv           base de exemplo
requirements.txt       dependencias do projeto
test_estoque.py        testes de produto, estoque e busca sequencial
test_tabela_hash.py    testes da tabela hash
resultados/            graficos gerados pelo benchmark
```
