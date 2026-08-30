import pytest

from estoque import Produto, validar_codigo_barras, validar_produto
from busca_sequencial import buscar_sequencial


def fazer_produtos():
    return [
        Produto("7891234567895", "Arroz", 40, 28.90),
        Produto("7890000000017", "Feijao", 8, 7.50),
        Produto("0788020123456", "Leite", 60, 4.99),
    ]


def test_produto_guarda_os_campos():
    p = Produto("7891234567895", "Arroz", 40, 28.90)
    assert p.codigo_barras == "7891234567895"
    assert p.nome == "Arroz"
    assert p.quantidade == 40
    assert p.preco == 28.90


def test_produtos_iguais_e_diferentes():
    a = Produto("7891234567895", "Arroz", 40, 28.90)
    b = Produto("7891234567895", "Arroz", 40, 28.90)
    c = Produto("7891234567895", "Arroz", 41, 28.90)
    assert a == b
    assert a != c
    assert a != "7891234567895"


def test_validar_produto_aceita_produto_valido():
    validar_produto(Produto("7891234567895", "Arroz", 40, 28.90))
    validar_produto(Produto("78912345", "Sal", 0, 0))


@pytest.mark.parametrize("codigo", [
    12345678,
    "789123",
    "789123456789012345",
    "789123A567895",
    "",
])
def test_validar_codigo_barras_rejeita_invalidos(codigo):
    with pytest.raises(ValueError):
        validar_codigo_barras(codigo)


@pytest.mark.parametrize("produto", [
    Produto("789123", "Arroz", 40, 28.90),
    Produto("7891234567895", "", 40, 28.90),
    Produto("7891234567895", "   ", 40, 28.90),
    Produto("7891234567895", "Arroz", -1, 28.90),
    Produto("7891234567895", "Arroz", 1.5, 28.90),
    Produto("7891234567895", "Arroz", True, 28.90),
    Produto("7891234567895", "Arroz", 40, -0.01),
    Produto("7891234567895", "Arroz", 40, "caro"),
])
def test_validar_produto_rejeita_invalidos(produto):
    with pytest.raises(ValueError):
        validar_produto(produto)


def test_busca_sequencial_primeiro_elemento():
    produtos = fazer_produtos()
    encontrado, comparacoes = buscar_sequencial(produtos, "7891234567895")
    assert encontrado is produtos[0]
    assert comparacoes == 1


def test_busca_sequencial_ultimo_elemento():
    produtos = fazer_produtos()
    encontrado, comparacoes = buscar_sequencial(produtos, "0788020123456")
    assert encontrado is produtos[-1]
    assert comparacoes == len(produtos)


def test_busca_sequencial_codigo_inexistente():
    produtos = fazer_produtos()
    encontrado, comparacoes = buscar_sequencial(produtos, "0000000000000")
    assert encontrado is None
    assert comparacoes == len(produtos)


def test_busca_sequencial_lista_vazia():
    encontrado, comparacoes = buscar_sequencial([], "7891234567895")
    assert encontrado is None
    assert comparacoes == 0
