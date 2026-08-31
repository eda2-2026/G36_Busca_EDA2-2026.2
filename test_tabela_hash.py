from tabela_hash import TabelaHash


def test_insere_e_busca_valor():
    tabela = TabelaHash()

    tabela.inserir("7891234567895", "Arroz")
    valor, comparacoes = tabela.buscar("7891234567895")

    assert valor == "Arroz"
    assert comparacoes == 1


def test_busca_valor_inexistente():
    tabela = TabelaHash()

    valor, comparacoes = tabela.buscar("0000000000000")

    assert valor is None
    assert comparacoes == 0


def test_trata_colisao_com_sondagem_linear():
    tabela = TabelaHash(capacidade=5)

    tabela.inserir("a", "Primeiro")
    tabela.inserir("f", "Segundo")

    valor, comparacoes = tabela.buscar("f")

    assert valor == "Segundo"
    assert comparacoes == 2


def test_atualiza_valor_quando_chave_ja_existe():
    tabela = TabelaHash()

    tabela.inserir("7891234567895", "Arroz")
    tabela.inserir("7891234567895", "Arroz tipo 1")

    valor, _ = tabela.buscar("7891234567895")

    assert valor == "Arroz tipo 1"
    assert tabela.tamanho == 1


def test_remove_sem_quebrar_busca_em_colisao():
    tabela = TabelaHash(capacidade=5)

    tabela.inserir("a", "Primeiro")
    tabela.inserir("f", "Segundo")
    removido, _ = tabela.remover("a")
    valor, comparacoes = tabela.buscar("f")

    assert removido == "Primeiro"
    assert valor == "Segundo"
    assert comparacoes == 1


def test_redimensiona_quando_fator_de_carga_fica_alto():
    tabela = TabelaHash(capacidade=3, fator_carga_maximo=0.7)

    tabela.inserir("1", "A")
    tabela.inserir("2", "B")
    tabela.inserir("3", "C")

    assert tabela.capacidade > 3
    assert tabela.buscar("1")[0] == "A"
    assert tabela.buscar("2")[0] == "B"
    assert tabela.buscar("3")[0] == "C"
