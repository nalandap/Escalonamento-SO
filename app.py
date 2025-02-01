from flask import Flask, render_template, request, jsonify
from escalonadores import fifo_scheduler, sjf_scheduler, round_robin_scheduler, edf_scheduler
from memoria import RAM, Disco
from substituicao import substituir_pagina_fifo, substituir_pagina_lru
from substituicao import simular_execucao

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
        'remaining_time': int(data['execution_time']) 
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

    @app.route('/adicionar_pagina', methods=['POST'])
    def adicionar_pagina():
        data = request.json
        nova_pagina = {
            'id': len(ram.paginas) + len(disco.paginas) + 1,
            '#ultimo_acesso': data.get('ultimo_acesso', 0)
        }
        algoritmo = data.get('algoritmo', 'FIFO')

        if algoritmo == 'FIFO':
            resultado = substituir_pagina_fifo(ram, disco, nova_pagina)
        elif algoritmo == 'LRU':
            resultado = substituir_pagina_lru(ram, disco, nova_pagina)
        else:
            return jsonify({'error': 'Algoritmo desconhecido'}), 400

        return jsonify({
            'message': resultado,
            'ram': str(ram),
            'disco': str(disco)})
 

processos = [
    {'id': 1, 'paginas': [{'id': i} for i in range(1, 16)]},  # 15 páginas
    {'id': 2, 'paginas': [{'id': i} for i in range(16, 31)]},  # 15 páginas
    {'id': 3, 'paginas': [{'id': i} for i in range(31, 46)]},  # 15 páginas
    {'id': 4, 'paginas': [{'id': i} for i in range(46, 61)]},  # 15 páginas → Agora RAM precisa substituir páginas
    {'id': 5, 'paginas': [{'id': i} for i in range(61, 76)]},  # 15 páginas → Mais substituições
]
simular_execucao(processos, 'LRU')  
if __name__ == '__main__':
    app.run(debug=True)
