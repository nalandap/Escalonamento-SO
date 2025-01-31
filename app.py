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
 
        'deadline': int(data['deadline']),
        'quantum': int(data['quantum']),
        'overhead': int(data['overhead']),
        'remaining_time': int(data['execution_time'])  # Inicializa o remaining_time
    }
    processes.append(process)
    return jsonify({'message': 'Processo adicionado com sucesso!'})

@app.route('/run_scheduler', methods=['POST'])
def run_scheduler():
    print("Requisição recebida no servidor!") 
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

    print("Resultado:", result)  
    return jsonify(result)

def fifo_scheduler():
    if not processes:
        return {'algorithm': 'FIFO', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

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

    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    return {'algorithm': 'FIFO', 'avg_turnaround': avg_turnaround}

def sjf_scheduler():
    if not processes:
        return {'algorithm': 'SJF', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    sorted_processes = sorted(processes, key=lambda x: (x['arrival_time'], x['execution_time']))

    current_time = 0
    turnaround_times = []
    ready_queue = []

    while sorted_processes or ready_queue:
        while sorted_processes and sorted_processes[0]['arrival_time'] <= current_time:
            ready_queue.append(sorted_processes.pop(0))

        if ready_queue:
            ready_queue.sort(key=lambda x: x['execution_time'])
            process = ready_queue.pop(0)

            start_time = current_time
            current_time += process['execution_time']
            end_time = current_time

            turnaround_time = end_time - process['arrival_time']
            turnaround_times.append(turnaround_time)
        else:
            current_time = sorted_processes[0]['arrival_time']

    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    return {'algorithm': 'SJF', 'avg_turnaround': avg_turnaround}



def round_robin_scheduler():
    if not processes:
        return {'algorithm': 'Round Robin', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    quantum = processes[0]['quantum'] 
    current_time = 0
    turnaround_times = []
    ready_queue = []
    remaining_processes = sorted(processes, key=lambda x: x['arrival_time'])  # Ordena por arrival_time

    while remaining_processes or ready_queue:
        # Adiciona processos que chegaram ao current_time na ready_queue
        while remaining_processes and remaining_processes[0]['arrival_time'] <= current_time:
            ready_queue.append(remaining_processes.pop(0))

        if ready_queue:
            process = ready_queue.pop(0)  # Pega o primeiro processo da fila de prontos

            # Executa o processo pelo tempo do quantum ou pelo tempo restante, o que for menor
            execution_time = min(quantum, process['remaining_time'])
            current_time += execution_time
            process['remaining_time'] -= execution_time

            # Se o processo ainda tem tempo restante, coloca de volta na fila de prontos
            if process['remaining_time'] > 0:
                ready_queue.append(process)
            else:
                # Processo concluído: calcula o turnaround
                turnaround_time = current_time - process['arrival_time']
                turnaround_times.append(turnaround_time)
        else:
            # Se não há processos prontos, avança o tempo para o próximo processo
            if remaining_processes:
                current_time = remaining_processes[0]['arrival_time']

    # Calcula o turnaround médio
    avg_turnaround = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
    return {'algorithm': 'Round Robin', 'avg_turnaround': avg_turnaround}
if __name__ == '__main__':
    app.run(debug=True)