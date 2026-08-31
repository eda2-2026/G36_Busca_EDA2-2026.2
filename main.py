import argparse

from estoque import CAMINHO_CSV_PADRAO, LIMITE_ESTOQUE_BAIXO_PADRAO, Estoque

MENU = """
=== EstoqueHash ===
1 - Cadastrar produto
2 - Buscar produto
3 - Registrar entrada
4 - Registrar saida
5 - Remover produto
6 - Listar produtos
7 - Alertas de estoque baixo
8 - Estatisticas da tabela hash
0 - Salvar e sair
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Controle de estoque com busca de produtos por tabela hash."
    )
    parser.add_argument("--dados", default=CAMINHO_CSV_PADRAO)
    parser.add_argument("--limite", type=int, default=LIMITE_ESTOQUE_BAIXO_PADRAO)
    return parser.parse_args()


def ler(texto):
    return input(texto).strip()


def ler_inteiro(texto):
    try:
        return int(ler(texto))
    except ValueError:
        raise ValueError("Digite um numero inteiro.")


def ler_float(texto):
    try:
        return float(ler(texto).replace(",", "."))
    except ValueError:
        raise ValueError("Digite um numero valido.")


def formatar_produto(produto):
    return (f"{produto.codigo_barras} | {produto.nome} | "
            f"qtd: {produto.quantidade} | R$ {produto.preco:.2f}")


def acao_cadastrar(estoque):
    produto = estoque.cadastrar(
        ler("Codigo de barras: "),
        ler("Nome: "),
        ler_inteiro("Quantidade: "),
        ler_float("Preco: "),
    )
    print(f"Cadastrado: {formatar_produto(produto)}")


def acao_buscar(estoque):
    produto, comparacoes = estoque.buscar(ler("Codigo de barras: "))
    if produto is None:
        print(f"Produto nao encontrado ({comparacoes} comparacoes).")
    else:
        print(f"{formatar_produto(produto)}  ({comparacoes} comparacoes)")


def acao_entrada(estoque):
    produto = estoque.registrar_entrada(
        ler("Codigo de barras: "), ler_inteiro("Quantidade de entrada: ")
    )
    print(f"Novo saldo: {produto.quantidade}")


def acao_saida(estoque):
    produto = estoque.registrar_saida(
        ler("Codigo de barras: "), ler_inteiro("Quantidade de saida: ")
    )
    print(f"Novo saldo: {produto.quantidade}")


def acao_remover(estoque):
    if estoque.remover(ler("Codigo de barras: ")):
        print("Produto removido.")
    else:
        print("Produto nao encontrado.")


def acao_listar(estoque):
    produtos = estoque.listar()
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
    for produto in produtos:
        print(formatar_produto(produto))
    print(f"Total: {len(produtos)} produto(s).")


def acao_alertas(estoque):
    produtos = estoque.alertas_estoque_baixo()
    if not produtos:
        print("Nenhum produto abaixo do limite.")
        return
    print(f"Produtos com quantidade <= {estoque.limite_estoque_baixo}:")
    for produto in produtos:
        print(formatar_produto(produto))


def acao_estatisticas(estoque):
    tabela = estoque.tabela
    print(f"Capacidade da tabela: {tabela.capacidade}")
    print(f"Produtos armazenados: {tabela.tamanho}")
    print(f"Fator de carga: {tabela.fator_carga:.2f}")


ACOES = {
    "1": acao_cadastrar,
    "2": acao_buscar,
    "3": acao_entrada,
    "4": acao_saida,
    "5": acao_remover,
    "6": acao_listar,
    "7": acao_alertas,
    "8": acao_estatisticas,
}


def main():
    args = parse_args()
    estoque = Estoque(limite_estoque_baixo=args.limite)
    total = estoque.carregar(args.dados)
    print(f"{total} produto(s) carregado(s) de {args.dados}.")

    while True:
        print(MENU)
        try:
            opcao = ler("Opcao: ")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrado sem salvar.")
            return

        if opcao == "0":
            estoque.salvar(args.dados)
            print(f"Dados salvos em {args.dados}.")
            return

        acao = ACOES.get(opcao)
        if acao is None:
            print("Opcao invalida.")
            continue

        try:
            acao(estoque)
        except ValueError as erro:
            print(f"Erro: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrado sem salvar.")
            return


if __name__ == "__main__":
    main()
