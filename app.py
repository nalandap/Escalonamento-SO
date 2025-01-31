from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


processes = []

#Variáveis globais para não requisitar sempre que adicionar um processo
quantum = None
overhead = None

@app.route('/')
def index():
    return render_template('index.html', quantum=quantum, overhead=overhead, process_list=processes)

@app.route('/set_config', methods=['POST'])
def set_config():
    """ Define o Quantum e a Sobrecarga do sistema uma única vez """
    global quantum, overhead
    data = request.json
    quantum = int(data.get('quantum', 1))  # Define um valor padrão caso esteja vazio
    overhead = int(data.get('overhead', 0))
    return jsonify({'message': 'Configurações salvas com sucesso!', 'quantum': quantum, 'overhead': overhead})

@app.route('/add_process', methods=['POST'])
def add_process():
    data = request.json
    process = {
        'pid': len(processes) + 1,
        'arrival_time': int(data['arrival_time']),
        'execution_time': int(data['execution_time']),
        'deadline': int(data['deadline'])
 
    }
    processes.append(process)
    return jsonify({'message': 'Processo adicionado com sucesso!'})

@app.route('/run_scheduler', methods=['POST'])
def run_scheduler():
    algorithm = request.json['algorithm']
    result = {}

    if algorithm == 'FIFO':
        result = fifo_scheduler()
    elif algorithm == 'SJF':
        result = sjf_scheduler()
    elif algorithm == 'Round Robin':
        if quantum is None:
            return jsonify({'error': 'Quantum não definido'}), 400
        result = round_robin_scheduler()
    elif algorithm == 'EDF':
        result = edf_scheduler()
    else:
        return jsonify({'error': 'Algoritmo desconhecido'}), 400

    return jsonify(result)

def fifo_scheduler():
    if not processes:
        return {'algorithm': 'FIFO', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    # Ordena os processos por tempo de chegada
    sorted_processes = sorted(processes, key=lambda x: x['arrival_time'])

    current_time = 0
    turnaround_times = []

    for process in sorted_processes:
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']

    
        start_time = current_time

        
        current_time += process['execution_time']

        
        end_time = current_time

       
        turnaround_time = end_time - process['arrival_time']
        turnaround_times.append(turnaround_time)

    # Calcula o turnaround médio
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    return {'algorithm': 'FIFO', 'avg_turnaround': avg_turnaround}

def sjf_scheduler():
    if not processes:
        return {'algorithm': 'SJF', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    # Ordena os processos por tempo de chegada e tempo de execução
    sorted_processes = sorted(processes, key=lambda x: (x['arrival_time'], x['execution_time']))

    current_time = 0
    turnaround_times = []
    ready_queue = []

    while sorted_processes or ready_queue:
        # Adiciona processos que já chegaram à fila de prontos
        while sorted_processes and sorted_processes[0]['arrival_time'] <= current_time:
            ready_queue.append(sorted_processes.pop(0))

        if ready_queue:
            # Escolhe o processo com o menor tempo de execução
            ready_queue.sort(key=lambda x: x['execution_time'])
            process = ready_queue.pop(0)

            # Executa o processo
            start_time = current_time
            current_time += process['execution_time']
            end_time = current_time

            # Calcula o turnaround
            turnaround_time = end_time - process['arrival_time']
            turnaround_times.append(turnaround_time)
        else:
            # Avança o tempo para o próximo processo
            current_time = sorted_processes[0]['arrival_time']

    # Calcula o turnaround médio
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    return {'algorithm': 'SJF', 'avg_turnaround': avg_turnaround}


def round_robin_scheduler():
    if not processes:
        return {'algorithm': 'Round Robin', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    current_time = 0
    turnaround_times = []
    ready_queue = processes.copy() 
    ready_queue.sort(key=lambda x: x['arrival_time']) 

    while ready_queue:
        process = ready_queue.pop(0)  

        
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']

       
        if process['remaining_time'] > quantum:
            current_time += quantum
            process['remaining_time'] -= quantum
            ready_queue.append(process)  
        else:
            current_time += process['remaining_time']
            process['remaining_time'] = 0
            turnaround_time = current_time - process['arrival_time']
            turnaround_times.append(turnaround_time)

    
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    return {'algorithm': 'Round Robin', 'avg_turnaround': avg_turnaround}
# Implementações para Round Robin e EDF podem ser adicionadas aqui

if __name__ == '__main__':
    app.run(debug=True)