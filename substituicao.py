from memoria import RAM, Disco
import time

def substituir_pagina_fifo(ram, disco, nova_pagina):
    pagina_removida = None
    if ram.esta_cheia():
        pagina_removida = ram.paginas.pop(0)  # Remove a primeira página (FIFO)
        disco.adicionar_pagina(pagina_removida)  # Move a página para o disco
        del ram.tempo_acesso[pagina_removida['id']]  # Remove o tempo de acesso
        
    ram.adicionar_pagina(nova_pagina)  # Adiciona a nova página na RAM
    return pagina_removida  # Retorna a página removida para que possa ser manipulada


def substituir_pagina_lru(ram, disco, nova_pagina):
    pagina_removida = None
    if ram.esta_cheia():
        # Encontra a página menos recentemente utilizada (LRU)
        pagina_lru = min(ram.tempo_acesso, key=ram.tempo_acesso.get)
        for pagina in ram.paginas:
            if pagina['id'] == pagina_lru:
                pagina_removida = pagina
                break
        ram.remover_pagina(pagina_removida)  # Remove a página da RAM
        disco.adicionar_pagina(pagina_removida)  # Move para o disco
    
    ram.adicionar_pagina(nova_pagina)  # Adiciona a nova página na RAM
    return pagina_removida  # Retorna a página removida para que possa ser manipulada
