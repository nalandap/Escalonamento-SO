# Sistema de Escalonamento de Processos

Este projeto implementa um sistema de escalonamento de processos que suporta múltiplos algoritmos de escalonamento e substituição de páginas. O sistema é desenvolvido em Python com uma interface web usando Flask.

## Funcionalidades

### FASE 1: Escalonamento de Processos

O sistema implementa os seguintes algoritmos de escalonamento de processos:

1. **FIFO (First-In, First-Out)**:
   - Executa os processos na ordem de chegada.
   - Não é preemptivo.

2. **SJF (Shortest Job First)**:
   - Executa o processo com o menor tempo de execução primeiro.
   - Ordena os processos por tempo de chegada e, em seguida, por tempo de execução para evitar starvation.

3. **Round Robin**:
   - Algoritmo preemptivo que atribui um tempo fixo (quantum) para cada processo.
   - Se um processo não terminar dentro do quantum, ele é suspenso e colocado no final da fila de prontos.

4. **EDF (Earliest Deadline First)**:
   - Executa o processo com o prazo mais próximo primeiro.
   - Adequado para sistemas de tempo real.

### FASE 2: Substituição de Páginas

O sistema também implementa algoritmos de substituição de páginas para gerenciamento de memória:

1. **FIFO (First-In, First-Out)**:
   - Substitui a página que está na memória há mais tempo.

2. **LRU (Least Recently Used)**:
   - Substitui a página que não foi usada há mais tempo.

### Funcionalidades Adicionais

- **Gráfico de Gantt**: Visualização da execução dos processos ao longo do tempo.
- **Gráfico de Uso de Memória**: Mostra as páginas presentes na RAM e no disco em tempo real.
- **Turnaround Médio**: Calcula o tempo médio de turnaround (tempo de espera + tempo de execução) para os processos.

---

## Requisitos

- Python 3.x
- Flask (para a interface web)
- Bibliotecas adicionais (se necessário): `matplotlib` para gráficos.

---

## Como Usar

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Instale as dependências:
   ```bash
  pip install -r requirements.txt

### Executando o Sistema

1. Inicie o servidor Flask:
    ```bash
    python app.py

2. Acesse a aplicação no navegador:
    ```bash
    http://127.0.0.1:5000/


### Adicionando Processos

1. Na interface web, insira os dados do processo:
   - Tempo de chegada
   - Tempo de execução
   - Deadline
   - Quantum 
   - Sobrecarga do sistema

2. Clique em "Adicionar Processo" para incluir o processo na lista.

### Executando o Escalonador

1. Selecione o algoritmo de escalonamento desejado (FIFO, SJF, Round Robin, EDF).

2. Clique em "Executar Escalonador" para ver o resultado.

### Visualizando Gráficos

- O gráfico de Gantt e o gráfico de uso de memória serão exibidos automaticamente após a execução do escalonador.