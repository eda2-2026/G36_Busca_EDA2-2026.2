import csv
import os

from tabela_hash import TabelaHash

TAMANHO_MIN_CODIGO = 8
TAMANHO_MAX_CODIGO = 14

CAMINHO_CSV_PADRAO = "produtos.csv"
CABECALHO_CSV = ["codigo_barras", "nome", "quantidade", "preco"]

LIMITE_ESTOQUE_BAIXO_PADRAO = 10


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


def _validar_quantidade_movimento(quantidade, rotulo):
    if isinstance(quantidade, bool) or not isinstance(quantidade, int):
        raise ValueError(f"A quantidade de {rotulo} deve ser um numero inteiro.")
    if quantidade <= 0:
        raise ValueError(f"A quantidade de {rotulo} deve ser maior que zero.")


class Estoque:
    def __init__(self, limite_estoque_baixo=LIMITE_ESTOQUE_BAIXO_PADRAO):
        self.tabela = TabelaHash()
        self.limite_estoque_baixo = limite_estoque_baixo

    def cadastrar(self, codigo_barras, nome, quantidade, preco):
        produto = Produto(codigo_barras, nome, quantidade, preco)
        validar_produto(produto)

        existente, _ = self.tabela.buscar(codigo_barras)
        if existente is not None:
            raise ValueError("Ja existe um produto com esse codigo de barras.")

        self.tabela.inserir(codigo_barras, produto)
        return produto

    def buscar(self, codigo_barras):
        validar_codigo_barras(codigo_barras)
        return self.tabela.buscar(codigo_barras)

    def registrar_entrada(self, codigo_barras, quantidade):
        _validar_quantidade_movimento(quantidade, "entrada")
        produto = self._obter(codigo_barras)
        produto.quantidade += quantidade
        return produto

    def registrar_saida(self, codigo_barras, quantidade):
        _validar_quantidade_movimento(quantidade, "saida")
        produto = self._obter(codigo_barras)
        if quantidade > produto.quantidade:
            raise ValueError("Quantidade de saida maior que o saldo em estoque.")
        produto.quantidade -= quantidade
        return produto

    def remover(self, codigo_barras):
        validar_codigo_barras(codigo_barras)
        produto, _ = self.tabela.remover(codigo_barras)
        return produto is not None

    def listar(self):
        return sorted(self.tabela.valores(), key=lambda produto: produto.codigo_barras)

    def alertas_estoque_baixo(self):
        return [
            produto for produto in self.listar()
            if produto.quantidade <= self.limite_estoque_baixo
        ]

    def carregar(self, caminho=CAMINHO_CSV_PADRAO):
        produtos = carregar_produtos(caminho)
        self.tabela = TabelaHash()
        for produto in produtos:
            validar_produto(produto)
            self.tabela.inserir(produto.codigo_barras, produto)
        return len(produtos)

    def salvar(self, caminho=CAMINHO_CSV_PADRAO):
        salvar_produtos(caminho, self.listar())

    def _obter(self, codigo_barras):
        validar_codigo_barras(codigo_barras)
        produto, _ = self.tabela.buscar(codigo_barras)
        if produto is None:
            raise ValueError("Produto nao encontrado.")
        return produto
