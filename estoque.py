TAMANHO_MIN_CODIGO = 8
TAMANHO_MAX_CODIGO = 14


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
