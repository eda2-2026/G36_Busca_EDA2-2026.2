import pytest

from estoque import (
    Estoque,
    Produto,
    buscar_por_hash,
    carregar_produtos,
    criar_indice_hash,
    validar_codigo_barras,
    validar_produto,
)
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


def test_cria_indice_hash_com_produtos():
    produtos = fazer_produtos()

    indice = criar_indice_hash(produtos)
    encontrado, comparacoes = buscar_por_hash(indice, "7890000000017")

    assert encontrado is produtos[1]
    assert comparacoes >= 1


def test_busca_hash_e_sequencial_encontram_mesmo_produto():
    produtos = fazer_produtos()
    indice = criar_indice_hash(produtos)

    encontrado_hash, _ = buscar_por_hash(indice, "0788020123456")
    encontrado_sequencial, _ = buscar_sequencial(produtos, "0788020123456")

    assert encontrado_hash is encontrado_sequencial


def estoque_povoado():
    estoque = Estoque(limite_estoque_baixo=10)
    for produto in fazer_produtos():
        estoque.cadastrar(
            produto.codigo_barras, produto.nome, produto.quantidade, produto.preco
        )
    return estoque


def test_cadastrar_e_buscar():
    estoque = estoque_povoado()
    encontrado, comparacoes = estoque.buscar("7890000000017")
    assert encontrado.nome == "Feijao"
    assert comparacoes >= 1


def test_cadastrar_codigo_duplicado_falha():
    estoque = estoque_povoado()
    with pytest.raises(ValueError):
        estoque.cadastrar("7891234567895", "Arroz outro", 1, 1.0)


def test_cadastrar_produto_invalido_falha():
    estoque = Estoque()
    with pytest.raises(ValueError):
        estoque.cadastrar("7891234567895", "Arroz", -5, 1.0)


def test_registrar_entrada_soma_quantidade():
    estoque = estoque_povoado()
    produto = estoque.registrar_entrada("7891234567895", 10)
    assert produto.quantidade == 50


def test_registrar_saida_subtrai_quantidade():
    estoque = estoque_povoado()
    produto = estoque.registrar_saida("7891234567895", 15)
    assert produto.quantidade == 25


def test_registrar_saida_maior_que_saldo_falha_e_mantem_saldo():
    estoque = estoque_povoado()
    with pytest.raises(ValueError):
        estoque.registrar_saida("7890000000017", 100)
    produto, _ = estoque.buscar("7890000000017")
    assert produto.quantidade == 8


@pytest.mark.parametrize("quantidade", [0, -3, 2.5, True])
def test_movimento_com_quantidade_invalida_falha(quantidade):
    estoque = estoque_povoado()
    with pytest.raises(ValueError):
        estoque.registrar_entrada("7891234567895", quantidade)


def test_movimento_em_produto_inexistente_falha():
    estoque = Estoque()
    with pytest.raises(ValueError):
        estoque.registrar_saida("7891234567895", 1)


def test_remover_produto():
    estoque = estoque_povoado()
    assert estoque.remover("7891234567895") is True
    encontrado, _ = estoque.buscar("7891234567895")
    assert encontrado is None
    assert estoque.remover("7891234567895") is False


def test_listar_retorna_ordenado_por_codigo():
    estoque = estoque_povoado()
    codigos = [produto.codigo_barras for produto in estoque.listar()]
    assert codigos == sorted(codigos)
    assert len(codigos) == 3


def test_alertas_estoque_baixo():
    estoque = Estoque(limite_estoque_baixo=10)
    estoque.cadastrar("7891234567895", "Acima", 11, 1.0)
    estoque.cadastrar("7890000000017", "NoLimite", 10, 1.0)
    estoque.cadastrar("0788020123456", "Abaixo", 3, 1.0)

    nomes = [produto.nome for produto in estoque.alertas_estoque_baixo()]
    assert "Abaixo" in nomes
    assert "NoLimite" in nomes
    assert "Acima" not in nomes


def test_carregar_e_salvar_round_trip(tmp_path):
    caminho = tmp_path / "produtos.csv"
    estoque = estoque_povoado()
    estoque.salvar(caminho)

    outro = Estoque()
    total = outro.carregar(caminho)

    assert total == 3
    assert outro.listar() == estoque.listar()
    recarregado, _ = outro.buscar("0788020123456")
    assert recarregado.codigo_barras == "0788020123456"


def test_carregar_arquivo_inexistente_retorna_vazio(tmp_path):
    estoque = Estoque()
    total = estoque.carregar(tmp_path / "nao_existe.csv")
    assert total == 0
    assert estoque.listar() == []
    assert carregar_produtos(tmp_path / "nao_existe.csv") == []
