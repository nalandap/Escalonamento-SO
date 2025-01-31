class RAM:
    def __init__(self, capacidade):
        self.capacidade = capacidade  # Capacidade em número de páginas
        self.paginas = []  # Lista de páginas na RAM

    def adicionar_pagina(self, pagina):
        """Adiciona uma página à RAM, se houver espaço."""
        if len(self.paginas) < self.capacidade:
            self.paginas.append(pagina)
            return True
        return False  # RAM cheia

    def remover_pagina(self, pagina):
        """Remove uma página da RAM."""
        if pagina in self.paginas:
            self.paginas.remove(pagina)
            return True
        return False  # Página não encontrada

    def esta_cheia(self):
        """Verifica se a RAM está cheia."""
        return len(self.paginas) >= self.capacidade

    def __str__(self):
        return f"RAM: {[pagina['id'] for pagina in self.paginas]}"


class Disco:
    def __init__(self):
        self.paginas = []  # Lista de páginas no Disco

    def adicionar_pagina(self, pagina):
        """Adiciona uma página ao Disco."""
        self.paginas.append(pagina)

    def remover_pagina(self, pagina):
        """Remove uma página do Disco."""
        if pagina in self.paginas:
            self.paginas.remove(pagina)
            return True
        return False  # Página não encontrada

    def __str__(self):
        return f"Disco: {[pagina['id'] for pagina in self.paginas]}"