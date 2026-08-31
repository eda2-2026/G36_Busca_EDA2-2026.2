import random

from busca_sequencial import buscar_sequencial
from estoque import Produto
from tabela_hash import TabelaHash


def chaves_que_colidem(capacidade, alvo, quantidade):
    referencia = TabelaHash(capacidade=capacidade)
    chaves = []
    numero = 0
    while len(chaves) < quantidade:
        chave = str(numero).zfill(13)
        if referencia.calcular_hash(chave) == alvo:
            chaves.append(chave)
        numero += 1
    return chaves


def caso_melhor_hash():
    tabela = TabelaHash(capacidade=101)
    tabela.inserir("7891234567895", "Arroz")
    _, comparacoes = tabela.buscar("7891234567895")
    return comparacoes


def caso_medio_hash():
    tabela = TabelaHash(capacidade=101)
    rng = random.Random(1)
    chaves = [str(rng.randrange(10 ** 12, 10 ** 13)) for _ in range(70)]
    for chave in chaves:
        tabela.inserir(chave, chave)
    comparacoes = [tabela.buscar(chave)[1] for chave in chaves]
    return sum(comparacoes) / len(comparacoes), max(comparacoes)


def caso_pior_hash(quantidade=40):
    tabela = TabelaHash(capacidade=101)
    tabela.fator_carga_maximo = float("inf")
    chaves = chaves_que_colidem(tabela.capacidade, 0, quantidade)
    for chave in chaves:
        tabela.inserir(chave, chave)
    _, comparacoes = tabela.buscar(chaves[-1])
    return len(chaves), comparacoes


def casos_busca_sequencial(n=100):
    produtos = [Produto(str(i).zfill(13), f"Produto {i}", 1, 1.0) for i in range(n)]
    melhor = buscar_sequencial(produtos, produtos[0].codigo_barras)[1]
    medio = buscar_sequencial(produtos, produtos[n // 2].codigo_barras)[1]
    pior = buscar_sequencial(produtos, "9999999999999")[1]
    return melhor, medio, pior


def main():
    print("=== Tabela hash ===\n")

    print("Melhor caso  (chave cai direto no indice, sem colisao)")
    print(f"  comparacoes: {caso_melhor_hash()}\n")

    media, maximo = caso_medio_hash()
    print("Caso medio   (70 chaves aleatorias, fator de carga ~0.7)")
    print(f"  comparacoes media: {media:.2f}")
    print(f"  comparacoes maximo: {maximo}\n")

    total, comparacoes = caso_pior_hash()
    print(f"Pior caso    ({total} chaves forcadas a colidir no mesmo indice, sem redimensionamento)")
    print(f"  comparacoes na ultima chave: {comparacoes}")
    print("  -> O(n): a busca percorre o cluster inteiro\n")

    melhor, medio, pior = casos_busca_sequencial()
    print("=== Busca sequencial (n = 100) ===\n")
    print(f"Melhor caso  (1a posicao):       {melhor}")
    print(f"Caso medio   (~n/2):             {medio}")
    print(f"Pior caso    (ausente / ultima): {pior}")


if __name__ == "__main__":
    main()
