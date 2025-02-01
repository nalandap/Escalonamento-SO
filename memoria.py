class RAM:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.paginas = []  
        self.tempo_acesso = {} 

    def adicionar_pagina(self, pagina):
        if len(self.paginas) * 4 < self.capacidade: 
            self.paginas.append(pagina)
            self.tempo_acesso[pagina['id']] = time.time()  
            return True
        return False

    def remover_pagina(self, pagina):
        if pagina in self.paginas:
            self.paginas.remove(pagina)
            del self.tempo_acesso[pagina['id']]
            return True
        return False

    def esta_cheia(self):
        return len(self.paginas) * 4 >= self.capacidade

    def __str__(self):
        return f"RAM: {[pagina['id'] for pagina in self.paginas]}"

class Disco:
    def __init__(self):
        self.paginas = []  # Lista de páginas no Disco

    def adicionar_pagina(self, pagina):
        self.paginas.append(pagina)

    def remover_pagina(self, pagina):
        if pagina in self.paginas:
            self.paginas.remove(pagina)
            return True
        return False

    def __str__(self):
        return f"Disco: {[pagina['id'] for pagina in self.paginas]}"