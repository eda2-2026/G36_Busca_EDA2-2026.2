import csv
import os

from tabela_hash import TabelaHash

TAMANHO_MIN_CODIGO = 8
TAMANHO_MAX_CODIGO = 14

CAMINHO_CSV_PADRAO = "produtos.csv"
CABECALHO_CSV = ["codigo_barras", "nome", "quantidade", "preco"]


class Produto:
    def __init__(self, codigo_barras, nome, quantidade, preco):
        self.codigo_barras = codigo_barras
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __eq__(self, other):
        if not isinstance(other, Produto):
            return NotImplemented
        return (self.codigo_barras == other.codigo_barras
                and self.nome == other.nome
                and self.quantidade == other.quantidade
                and self.preco == other.preco)

    def __repr__(self):
        return (f"Produto(codigo_barras={self.codigo_barras!r}, nome={self.nome!r}, "
                f"quantidade={self.quantidade}, preco={self.preco})")


def validar_codigo_barras(codigo_barras):
    if not isinstance(codigo_barras, str):
        raise ValueError("O codigo de barras deve ser uma string.")
    if not codigo_barras.isdigit():
        raise ValueError("O codigo de barras deve conter apenas digitos.")
    if not TAMANHO_MIN_CODIGO <= len(codigo_barras) <= TAMANHO_MAX_CODIGO:
        raise ValueError(
            f"O codigo de barras deve ter entre {TAMANHO_MIN_CODIGO} e "
            f"{TAMANHO_MAX_CODIGO} digitos."
        )


def validar_produto(produto):
    validar_codigo_barras(produto.codigo_barras)

    if not isinstance(produto.nome, str) or not produto.nome.strip():
        raise ValueError("O nome do produto nao pode ser vazio.")

    if isinstance(produto.quantidade, bool) or not isinstance(produto.quantidade, int):
        raise ValueError("A quantidade deve ser um numero inteiro.")
    if produto.quantidade < 0:
        raise ValueError("A quantidade nao pode ser negativa.")

    if isinstance(produto.preco, bool) or not isinstance(produto.preco, (int, float)):
        raise ValueError("O preco deve ser um numero.")
    if produto.preco < 0:
        raise ValueError("O preco nao pode ser negativo.")


def carregar_produtos(caminho=CAMINHO_CSV_PADRAO):
    if not os.path.exists(caminho):
        return []

    produtos = []
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            codigo = (linha.get("codigo_barras") or "").strip()
            if not codigo:
                continue
            produtos.append(Produto(
                codigo,
                (linha.get("nome") or "").strip(),
                int(linha["quantidade"]),
                float(linha["preco"]),
            ))
    return produtos


def salvar_produtos(caminho, produtos):
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(CABECALHO_CSV)
        for produto in produtos:
            escritor.writerow([
                produto.codigo_barras,
                produto.nome,
                produto.quantidade,
                f"{produto.preco:.2f}",
            ])


def criar_indice_hash(produtos):
    tabela_hash = TabelaHash()

    for produto in produtos:
        validar_produto(produto)
        tabela_hash.inserir(produto.codigo_barras, produto)

    return tabela_hash


def buscar_por_hash(tabela_hash, codigo_barras):
    validar_codigo_barras(codigo_barras)
    return tabela_hash.buscar(codigo_barras)
