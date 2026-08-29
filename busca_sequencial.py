def buscar_sequencial(produtos, codigo_barras):
    comparacoes = 0
    for produto in produtos:
        comparacoes += 1
        if produto.codigo_barras == codigo_barras:
            return produto, comparacoes
    return None, comparacoes
