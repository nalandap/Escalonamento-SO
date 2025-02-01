from memoria import RAM, Disco

def substituir_pagina_fifo(ram, disco, nova_pagina):
    if ram.esta_cheia():
        pagina_removida = ram.paginas.pop(0)  # Remove a primeira página (FIFO)
        disco.adicionar_pagina(pagina_removida)
    ram.adicionar_pagina(nova_pagina)

# Função para substituição de páginas usando LRU
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

def simular_execucao(processos, algoritmo):
    ram = RAM(200)  # 200 KB de RAM
    disco = Disco()
    turnaround_total = 0
    tempo_inicio = time.time()

    for processo in processos:
        print(f"Executando processo {processo['id']} com páginas: {[pagina['id'] for pagina in processo['paginas']]}")
        for pagina in processo['paginas']:
            if not ram.adicionar_pagina(pagina):
                if algoritmo == 'FIFO':
                    substituir_pagina_fifo(ram, disco, pagina)
                elif algoritmo == 'LRU':
                    substituir_pagina_lru(ram, disco, pagina)
            time.sleep(0.1)  # Delay para simular o tempo de execução
        turnaround_total += time.time() - tempo_inicio
        print(ram)
        print(disco)
        print(f"Turnaround parcial: {time.time() - tempo_inicio:.2f} segundos\n")

    print(f"Turnaround médio: {turnaround_total / len(processos):.2f} segundos")    
