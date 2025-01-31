from memoria import RAM, Disco
from substituicao import fifo_substituicao, lru_substituicao

# Inicializa a RAM (capacidade de 3 páginas) e o Disco
ram = RAM(capacidade=3)
disco = Disco()

# Páginas de exemplo
pagina1 = {'id': 1, 'ultimo_acesso': 0}
pagina2 = {'id': 2, 'ultimo_acesso': 1}
pagina3 = {'id': 3, 'ultimo_acesso': 2}
pagina4 = {'id': 4, 'ultimo_acesso': 3}

# Adiciona páginas à RAM
print(fifo_substituicao(ram, disco, pagina1))  # Adiciona página 1 à RAM
print(fifo_substituicao(ram, disco, pagina2))  # Adiciona página 2 à RAM
print(fifo_substituicao(ram, disco, pagina3))  # Adiciona página 3 à RAM

# RAM está cheia, substitui a página mais antiga (FIFO)
print(fifo_substituicao(ram, disco, pagina4))  # Substitui página 1 por página 4

# Exibe o estado da RAM e do Disco
print(ram)  # RAM: [2, 3, 4]
print(disco)  # Disco: [1]