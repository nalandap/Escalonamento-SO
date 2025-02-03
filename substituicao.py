from memoria import RAM, Disco
import time

def substituir_pagina_fifo(ram, disco, nova_pagina):
    if ram.esta_cheia():
        pagina_removida = ram.paginas.pop(0)  
        disco.adicionar_pagina(pagina_removida)
        del ram.tempo_acesso[pagina_removida['id']] 
    
    ram.adicionar_pagina(nova_pagina)  



def substituir_pagina_lru(ram, disco, nova_pagina):
    if ram.esta_cheia():
        # Encontra a página menos recentemente utilizada
        pagina_lru = min(ram.tempo_acesso, key=ram.tempo_acesso.get)
        for pagina in ram.paginas:
            if pagina['id'] == pagina_lru:
                pagina_removida = pagina
                break
        ram.remover_pagina(pagina_removida)
        disco.adicionar_pagina(pagina_removida)
    ram.adicionar_pagina(nova_pagina)


    
