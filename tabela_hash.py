class TabelaHash:
    def __init__(self, capacidade=11):
        if capacidade <= 0:
            raise ValueError("A capacidade deve ser maior que zero.")

        self.capacidade = capacidade
        self.tabela = [None] * self.capacidade
        self.tamanho = 0

    def calcular_hash(self, chave):
        valor_hash = 0

        for caractere in str(chave):
            valor_hash = (valor_hash * 31 + ord(caractere)) % self.capacidade

        return valor_hash
