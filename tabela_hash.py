class _Removido:
    pass


REMOVIDO = _Removido()


class TabelaHash:
    def __init__(self, capacidade=11, fator_carga_maximo=0.7):
        if capacidade <= 0:
            raise ValueError("A capacidade deve ser maior que zero.")

        self.capacidade = self._proximo_primo(capacidade)
        self.fator_carga_maximo = fator_carga_maximo
        self.tabela = [None] * self.capacidade
        self.tamanho = 0

    @property
    def fator_carga(self):
        return self.tamanho / self.capacidade

    def calcular_hash(self, chave):
        valor_hash = 0

        for caractere in str(chave):
            valor_hash = (valor_hash * 31 + ord(caractere)) % self.capacidade

        return valor_hash

    def inserir(self, chave, valor):
        if (self.tamanho + 1) / self.capacidade > self.fator_carga_maximo:
            self._redimensionar()

        indice, encontrado, comparacoes = self._encontrar_posicao(chave)
        self.tabela[indice] = (str(chave), valor)

        if not encontrado:
            self.tamanho += 1

        return comparacoes

    def buscar(self, chave):
        indice_inicial = self.calcular_hash(chave)
        comparacoes = 0

        for tentativa in range(self.capacidade):
            indice = (indice_inicial + tentativa) % self.capacidade
            item = self.tabela[indice]

            if item is None:
                return None, comparacoes

            if item is REMOVIDO:
                continue

            chave_atual, valor = item
            comparacoes += 1

            if chave_atual == str(chave):
                return valor, comparacoes

        return None, comparacoes

    def remover(self, chave):
        indice_inicial = self.calcular_hash(chave)
        comparacoes = 0

        for tentativa in range(self.capacidade):
            indice = (indice_inicial + tentativa) % self.capacidade
            item = self.tabela[indice]

            if item is None:
                return None, comparacoes

            if item is REMOVIDO:
                continue

            chave_atual, valor = item
            comparacoes += 1

            if chave_atual == str(chave):
                self.tabela[indice] = REMOVIDO
                self.tamanho -= 1
                return valor, comparacoes

        return None, comparacoes

    def itens(self):
        for item in self.tabela:
            if item is not None and item is not REMOVIDO:
                yield item

    def valores(self):
        for _, valor in self.itens():
            yield valor

    def _encontrar_posicao(self, chave):
        indice_inicial = self.calcular_hash(chave)
        primeiro_removido = None
        comparacoes = 0

        for tentativa in range(self.capacidade):
            indice = (indice_inicial + tentativa) % self.capacidade
            item = self.tabela[indice]

            if item is None:
                if primeiro_removido is not None:
                    return primeiro_removido, False, comparacoes
                return indice, False, comparacoes

            if item is REMOVIDO:
                if primeiro_removido is None:
                    primeiro_removido = indice
                continue

            chave_atual, _ = item
            comparacoes += 1

            if chave_atual == str(chave):
                return indice, True, comparacoes

        if primeiro_removido is not None:
            return primeiro_removido, False, comparacoes

        raise RuntimeError("Tabela hash cheia.")

    def _redimensionar(self):
        itens_antigos = list(self.itens())
        self.capacidade = self._proximo_primo(self.capacidade * 2)
        self.tabela = [None] * self.capacidade
        self.tamanho = 0

        for chave, valor in itens_antigos:
            self.inserir(chave, valor)

    def _proximo_primo(self, numero):
        while not self._eh_primo(numero):
            numero += 1
        return numero

    def _eh_primo(self, numero):
        if numero < 2:
            return False
        if numero == 2:
            return True
        if numero % 2 == 0:
            return False

        divisor = 3
        while divisor * divisor <= numero:
            if numero % divisor == 0:
                return False
            divisor += 2

        return True
