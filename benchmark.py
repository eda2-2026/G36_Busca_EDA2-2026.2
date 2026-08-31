import argparse
import os
import random
import statistics
import time

from busca_sequencial import buscar_sequencial
from estoque import Produto, criar_indice_hash

PASTA_RESULTADOS = "resultados"


def gerar_produtos(n, seed=42):
    rng = random.Random(seed)
    vistos = set()
    produtos = []
    while len(produtos) < n:
        codigo = "".join(rng.choice("0123456789") for _ in range(13))
        if codigo in vistos:
            continue
        vistos.add(codigo)
        produtos.append(Produto(
            codigo,
            f"Produto {len(produtos)}",
            rng.randint(0, 500),
            round(rng.uniform(1, 500), 2),
        ))
    return produtos


def gerar_consultas(produtos, k, frac_existentes=0.5, seed=7):
    rng = random.Random(seed)
    existentes = [produto.codigo_barras for produto in produtos]
    conhecidos = set(existentes)

    quantidade_existentes = int(k * frac_existentes)
    consultas = [rng.choice(existentes) for _ in range(quantidade_existentes)]

    while len(consultas) < k:
        codigo = "".join(rng.choice("0123456789") for _ in range(13))
        if codigo not in conhecidos:
            consultas.append(codigo)

    rng.shuffle(consultas)
    return consultas


def medir(busca, consultas, repeticoes):
    for codigo in consultas:
        busca(codigo)

    tempos = []
    comparacoes_soma = 0
    comparacoes_max = 0
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        soma = 0
        pico = 0
        for codigo in consultas:
            _, comparacoes = busca(codigo)
            soma += comparacoes
            if comparacoes > pico:
                pico = comparacoes
        tempos.append((time.perf_counter() - inicio) / len(consultas))
        comparacoes_soma = soma
        comparacoes_max = max(comparacoes_max, pico)

    return {
        "tempo_medio_us": statistics.mean(tempos) * 1_000_000,
        "comparacoes_media": comparacoes_soma / len(consultas),
        "comparacoes_max": comparacoes_max,
    }


def rodar_experimento(tamanhos, k, repeticoes):
    resultados = []
    for n in tamanhos:
        produtos = gerar_produtos(n)
        consultas = gerar_consultas(produtos, k)
        tabela = criar_indice_hash(produtos)

        medida_hash = medir(lambda codigo: tabela.buscar(codigo), consultas, repeticoes)
        medida_seq = medir(
            lambda codigo: buscar_sequencial(produtos, codigo), consultas, repeticoes
        )

        resultados.append({"n": n, "algoritmo": "hash", **medida_hash})
        resultados.append({"n": n, "algoritmo": "sequencial", **medida_seq})
    return resultados


def imprimir_tabela(resultados):
    cabecalho = f"{'n':>8} | {'algoritmo':>11} | {'comp. media':>12} | {'comp. max':>9} | {'tempo (us)':>10}"
    print(cabecalho)
    print("-" * len(cabecalho))
    for linha in resultados:
        print(
            f"{linha['n']:>8} | {linha['algoritmo']:>11} | "
            f"{linha['comparacoes_media']:>12.2f} | {linha['comparacoes_max']:>9} | "
            f"{linha['tempo_medio_us']:>10.2f}"
        )


def plotar(resultados, pasta=PASTA_RESULTADOS):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(pasta, exist_ok=True)
    tamanhos = sorted({linha["n"] for linha in resultados})

    def serie(algoritmo, chave):
        return [
            next(
                linha[chave]
                for linha in resultados
                if linha["n"] == n and linha["algoritmo"] == algoritmo
            )
            for n in tamanhos
        ]

    plt.figure()
    plt.plot(tamanhos, serie("hash", "comparacoes_media"), marker="o", label="Tabela hash")
    plt.plot(tamanhos, serie("sequencial", "comparacoes_media"), marker="o", label="Busca sequencial")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Numero de produtos (n)")
    plt.ylabel("Comparacoes medias por busca")
    plt.title("Comparacoes: hash x sequencial")
    plt.legend()
    plt.grid(True, which="both", linestyle=":")
    plt.savefig(os.path.join(pasta, "comparacoes.png"), dpi=120, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.plot(tamanhos, serie("hash", "tempo_medio_us"), marker="o", label="Tabela hash")
    plt.plot(tamanhos, serie("sequencial", "tempo_medio_us"), marker="o", label="Busca sequencial")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Numero de produtos (n)")
    plt.ylabel("Tempo medio por busca (us)")
    plt.title("Tempo: hash x sequencial")
    plt.legend()
    plt.grid(True, which="both", linestyle=":")
    plt.savefig(os.path.join(pasta, "tempo.png"), dpi=120, bbox_inches="tight")
    plt.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compara busca por tabela hash e busca sequencial."
    )
    parser.add_argument("--tamanhos", type=int, nargs="+", default=[100, 1000, 10000])
    parser.add_argument("--consultas", type=int, default=1000)
    parser.add_argument("--repeticoes", type=int, default=5)
    parser.add_argument("--sem-graficos", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    resultados = rodar_experimento(args.tamanhos, args.consultas, args.repeticoes)
    imprimir_tabela(resultados)
    if not args.sem_graficos:
        plotar(resultados)
        print(f"\nGraficos salvos em {PASTA_RESULTADOS}/comparacoes.png e {PASTA_RESULTADOS}/tempo.png")


if __name__ == "__main__":
    main()
