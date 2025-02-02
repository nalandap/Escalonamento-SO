from flask import Flask, render_template, request, jsonify
from escalonadores import fifo_scheduler, sjf_scheduler, round_robin_scheduler, edf_scheduler
from memoria import RAM, Disco
from substituicao import substituir_pagina_fifo, substituir_pagina_lru

app = Flask(__name__)

processes = []
quantum = None
overhead = None

# Dados globais para a Fase 2 (Substituição de Páginas)
ram = RAM(capacidade=50)  
disco = Disco()

# Rotas da Fase 1
@app.route('/')
def index():
    return render_template('index_fase1.html', quantum=quantum, overhead=overhead, process_list=processes)

@app.route('/set_config', methods=['POST'])
def set_config():
    """ Define o Quantum e a Sobrecarga do sistema uma única vez """
    global quantum, overhead
    data = request.json
    quantum = int(data.get('quantum', 0))  
    overhead = int(data.get('overhead', 0))
    return jsonify({'message': 'Configurações salvas com sucesso!', 'quantum': quantum, 'overhead': overhead})

@app.route('/add_process', methods=['POST'])
def add_process():
    data = request.json
    pid = len(processes) + 1  # Gera o número do processo

    process = {
        'pid': pid,
        'arrival_time': int(data['arrival_time']),
        'execution_time': int(data['execution_time']),
        'deadline': int(data['deadline']),
        'remaining_time': int(data['execution_time']),
        'qtd_paginas':int(data['qtd_paginas']),
        'paginas': list(map(int, data['paginas']))
    }
    processes.append(process)
    return jsonify({'message': 'Processo adicionado com sucesso!', 'pid': pid})

@app.route('/run_scheduler', methods=['POST'])
def run_scheduler():
    algorithm = request.json['algorithm']
    result = {}

    if algorithm == 'FIFO':
        result = fifo_scheduler(processes)
    elif algorithm == 'SJF':
        result = sjf_scheduler(processes)
    elif algorithm == 'Round Robin':
        if quantum is None:
            return jsonify({'error': 'Quantum não definido'}), 400
        result = round_robin_scheduler(processes, quantum, overhead)
    elif algorithm == 'EDF':
        result = edf_scheduler(processes, quantum, overhead)
    else:
        return jsonify({'error': 'Algoritmo desconhecido'}), 400

    result["gantt_chart"] = generate_gantt_chart(result, processes)
    return jsonify(result)

# Exportação Gráfico de Gantt

def generate_gantt_chart(result, processes):
    timeline = []
    for process in processes:
        gantt_row = {"process": f"P{process['pid']}", "states": []}
        for time in range(result['total_time']):
            if time < process['arrival_time']:
                gantt_row["states"].append("Cinza")
            elif time in result['executed'][process['pid']]:
                if time >= process['deadline']:  # Se ultrapassar o deadline, marcar como vermelho
                    gantt_row["states"].append("Vermelho")
                else:
                    gantt_row["states"].append("Lilás")
            elif time in result['waiting'][process['pid']]:
                gantt_row["states"].append("Amarelo")
            elif time in result['overhead'][process['pid']]:
                gantt_row["states"].append("Rosa")
            else:
                gantt_row["states"].append("Cinza")
        timeline.append(gantt_row)
    return timeline



    # Rotas da Fase 2
    @app.route('/')
    def fase2():
        return render_template('index_fase2.html')
 
    @app.route('/adicionarpaginas', methods=['POST'])
    def gerar_paginas_aleatorias(processos, max_pagina_id=1000):
        for processo in processos:
            qtd_paginas = processo.get('qtd_paginas', 0)

           
            if 1 <= qtd_paginas <= 10:
                processo['paginas'] = random.sample(range(1, max_pagina_id), qtd_paginas)
            else:
                processo['paginas'] = [] 

    
    
    @app.route('/paginação', methods=['POST'])
    def paginacao():
        turnaround_total = 0 
        tempo_inicio = time.time() 

        for processo in processos:
            if not processo['paginas']: 
                print(f"Processo {processo['id']} ignorado: não possui páginas.")
                continue
            
            if len(processo['paginas']) <= 10: 
                print(f"Processo {processo['id']} ignorado: possui 10 ou menos páginas.")
                continue

            print(f"Executando processo {processo['id']} com páginas: {[pagina['id'] for pagina in processo['paginas']]}")

            for pagina in processo['paginas']:
                if not ram.adicionar_pagina(pagina):
                    if algoritmo == 'FIFO':
                        substituir_pagina_fifo(ram, disco, pagina)
                    elif algoritmo == 'LRU':
                        substituir_pagina_lru(ram, disco, pagina)
                time.sleep(0.1) 

            turnaround_total += time.time() - tempo_inicio
            print(ram)
            print(disco)
            print(f"Turnaround parcial: {time.time() - tempo_inicio:.2f} segundos\n")

        if len(processos) > 0:
            print(f"Turnaround médio: {turnaround_total / len(processos):.2f} segundos")
        else:
            print("Nenhum processo foi executado.")  # Caso todos sejam ignorados




