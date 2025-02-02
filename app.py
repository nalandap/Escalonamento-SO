from flask import Flask, render_template, request, jsonify
import random
import time
from escalonadores import fifo_scheduler, sjf_scheduler, round_robin_scheduler, edf_scheduler
from memoria import RAM, Disco
from substituicao import substituir_pagina_fifo, substituir_pagina_lru
import copy

app = Flask(__name__)

processes = []
quantum = None
overhead = None
processes_copy = copy.deepcopy(processes)

# Dados globais para a Fase 2 (Substituição de Páginas)
ram = RAM(capacidade=50)
disco = Disco()

@app.route('/executar-substituicao', methods=['POST'])
def executar_substituicao():
    data = request.json
    algoritmo = data.get('algoritmo', 'FIFO')  
    pagina = data.get('pagina')

    if not pagina:
        return jsonify({"error": "Nenhuma página foi enviada"}), 400

    if algoritmo == 'FIFO':
        substituir_pagina_fifo(ram, disco, {'id': pagina})
    elif algoritmo == 'LRU':
        substituir_pagina_lru(ram, disco, {'id': pagina})
    else:
        return jsonify({"error": "Algoritmo inválido"}), 400

    return jsonify({"message": f"Substituição de páginas executada com {algoritmo}!"})

# --------------------- Função para gerar páginas aleatórias ---------------------

def gerar_paginas_aleatorias(processos, max_pagina_id=1000):
    for processo in processos:
        qtd_paginas = processo.get('qtd_paginas', 0)

        if 1 <= qtd_paginas <= 10:
            processo['paginas'] = random.sample(range(1, max_pagina_id), qtd_paginas)
        else:
            processo['paginas'] = [] 

# --------------------- Rotas da Fase 1 ---------------------

@app.route('/')
def index():
    return render_template('index_fase1.html', quantum=quantum, overhead=overhead, process_list=processes_copy)

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
    pid = len(processes_copy) + 1  # Gera o número do processo

    process = {
        'pid': pid,
        'arrival_time': int(data['arrival_time']),
        'execution_time': int(data['execution_time']),
        'deadline': int(data['deadline']),
        'remaining_time': int(data['execution_time']),
        'qtd_paginas': int(data.get('qtd_paginas', 0)),  
        'paginas': []
    }

    processes_copy.append(process)
    if process['qtd_paginas'] > 0:  
        gerar_paginas_aleatorias([process])

    return jsonify({'message': 'Processo adicionado com sucesso!', 'pid': pid, 'paginas': process['paginas']})

@app.route('/run_scheduler', methods=['POST'])
def run_scheduler():
    algorithm = request.json['algorithm']
    result = {}

    if algorithm == 'FIFO':
        result = fifo_scheduler(processes_copy)
    elif algorithm == 'SJF':
        result = sjf_scheduler(processes_copy)
    elif algorithm == 'Round Robin':
        if quantum is None:
            return jsonify({'error': 'Quantum não definido'}), 400
        result = round_robin_scheduler(processes_copy, quantum, overhead)
    elif algorithm == 'EDF':
        result = edf_scheduler(processes_copy, quantum, overhead)
    else:
        return jsonify({'error': 'Algoritmo desconhecido'}), 400

    result["gantt_chart"] = generate_gantt_chart(result, processes_copy)
    return jsonify(result)

# --------------------- Função para gerar gráfico de Gantt ---------------------

def generate_gantt_chart(result, processes):
    timeline = []
    for process in processes:
        gantt_row = {"process": f"P{process['pid']}", "states": []}
        for time in range(result['total_time']):
            if time < process['arrival_time']:
                gantt_row["states"].append("Cinza")
            elif time in result['executed'][process['pid']]:
                if time >= process['deadline']:
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

# --------------------- Rotas da Fase 2 ---------------------

#@app.route('/fase2')
#def fase2():
    #return render_template('index_fase2.html')

@app.route('/adicionarpaginas', methods=['POST'])
def adicionar_paginas():
    processos_com_paginas = [p for p in processes_copy if p.get('qtd_paginas', 0) > 0]
    gerar_paginas_aleatorias(processos_com_paginas)
    return jsonify({'message': 'Páginas geradas com sucesso!'})

@app.route('/paginacao', methods=['POST'])
@app.route('/paginacao', methods=['POST'])
def paginacao():
    data = request.json
    algoritmo = data.get('algoritmo', 'FIFO')  

   
    if ram is None or disco is None:
        return jsonify({'message': 'Erro: RAM ou Disco não foram inicializados corretamente.'}), 500

   
    processos_com_paginas = [p for p in processes_copy if p.get('paginas', [])]
    if not processos_com_paginas:
        return jsonify({'message': 'Nenhum processo com páginas cadastradas para a simulação.'}), 400

    turnaround_times = [] 

    for processo in processos_com_paginas:
        tempo_processo = time.time() 

        print(f"Executando processo {processo['pid']} com páginas: {processo['paginas']}")

        for pagina in processo['paginas']:
            if not ram.adicionar_pagina({'id': pagina}):  
                print(f"Falta de página detectada para {pagina}. Realizando substituição ({algoritmo})...")

                # AUTOMATICAMENTE EXECUTA A SUBSTITUIÇÃO QUANDO NECESSÁRIO
                if algoritmo == 'FIFO':
                    substituir_pagina_fifo(ram, disco, {'id': pagina})
                elif algoritmo == 'LRU':
                    substituir_pagina_lru(ram, disco, {'id': pagina})

            time.sleep(0.1) 

        turnaround_times.append(time.time() - tempo_processo) 

    turnaround_medio = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0

    return jsonify({
        'message': 'Paginação concluída!',
        'turnaround_medio': round(turnaround_medio, 2),
        'ram': [p['id'] for p in ram.paginas],  
        'disco': [p['id'] for p in disco.paginas]
    })
# --------------------- Teste manual de geração de páginas ---------------------

if __name__ == '__main__':
    app.run(debug=True)
