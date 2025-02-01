import time

class RAM:
    def __init__(self, capacidade):
        self.capacidade = capacidade  # Capacidade em MB (1 página = 4 MB)
        self.paginas = []  # Lista de páginas na RAM
        self.tempo_acesso = {}  # Dicionário para rastrear o tempo de acesso das páginas

    def adicionar_pagina(self, pagina):
        if len(self.paginas) * 4 < self.capacidade:  # Verifica se há espaço na RAM
            self.paginas.append(pagina)
            self.tempo_acesso[pagina['id']] = time.time()  # Atualiza o tempo de acesso
            return True
        return False

    def remover_pagina(self, pagina):
        if pagina in self.paginas:
            self.paginas.remove(pagina)
            del self.tempo_acesso[pagina['id']]  # Remove o tempo de acesso
            return True
        return False

    def substituir_pagina(self, nova_pagina):
        if self.esta_cheia():
            # Encontra a página mais antiga (FIFO)
            pagina_mais_antiga = min(self.tempo_acesso, key=self.tempo_acesso.get)
            for pagina in self.paginas:
                if pagina['id'] == pagina_mais_antiga:
                    pagina_removida = pagina
                    self.remover_pagina(pagina_removida)
                    self.adicionar_pagina(nova_pagina)
                    return pagina_removida  # Retorna a página removida para ser movida para o disco
        return None

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


