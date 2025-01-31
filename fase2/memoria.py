class RAM:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.paginas = []

    def adicionar_pagina(self, pagina):
        if len(self.paginas) < self.capacidade:
            self.paginas.append(pagina)
        else:
            raise Exception("RAM cheia")

class Disco:
    def __init__(self):
        self.paginas = []

    def adicionar_pagina(self, pagina):
        self.paginas.append(pagina)