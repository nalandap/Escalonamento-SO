import time

class RAM:
    def __init__(self, capacidade):
        self.capacidade = capacidade 
        self.paginas = []  
        self.tempo_acesso = {}  

    def adicionar_pagina(self, pagina):
        if self.esta_cheia():
            return False  
        
        self.paginas.append(pagina)
        self.tempo_acesso[pagina['id']] = time.time()  
        return True

    def esta_cheia(self):
        max_paginas =  200 // 4  # Cada página ocupa 4 KB
        return len(self.paginas) >= max_paginas


    def __str__(self):
        return f"RAM: {[pagina['id'] for pagina in self.paginas]}"


class Disco:
    def __init__(self):
        self.paginas = []  

    def adicionar_pagina(self, pagina):
        self.paginas.append(pagina)

    def remover_pagina(self, pagina):
        if pagina in self.paginas:
            self.paginas.remove(pagina)
            return True
        return False

    def __str__(self):
        return f"Disco: {[pagina['id'] for pagina in self.paginas]}"


