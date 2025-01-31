from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

processes = []
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
        'deadline': int(data['deadline']),
        'remaining_time': int(data['execution_time']) 
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

    sorted_processes = sorted(processes, key=lambda x: x['arrival_time'])

    current_time = 0
    turnaround_times = []

    for process in sorted_processes:
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']

        current_time += process['execution_time']
        turnaround_times.append(current_time - process['arrival_time'])

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
            current_time += process['execution_time']
            turnaround_times.append(current_time - process['arrival_time'])
        else:
            if sorted_processes:
                current_time = sorted_processes[0]['arrival_time']

    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    return {'algorithm': 'SJF', 'avg_turnaround': avg_turnaround}

def round_robin_scheduler():
    global quantum
    if not processes:
        return {'algorithm': 'Round Robin', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    for process in processes:
        process['remaining_time'] = process['execution_time']
        process['waiting_time'] = 0  

    current_time = 0
    turnaround_times = []
    ready_queue = []
    remaining_processes = sorted(processes, key=lambda x: x['arrival_time'])  

    while remaining_processes or ready_queue:
        while remaining_processes and remaining_processes[0]['arrival_time'] <= current_time:
            process = remaining_processes.pop(0)
            ready_queue.append(process)
            print(f"Processo {process['pid']} adicionado à fila de prontos no tempo {current_time}")

        if ready_queue:
            ready_queue.sort(key=lambda x: -x['waiting_time'])  
            process = ready_queue.pop(0)  

            
            execution_time = min(quantum, process['remaining_time'])
            for _ in range(execution_time):
                current_time += 1
                process['remaining_time'] -= 1

                
                while remaining_processes and remaining_processes[0]['arrival_time'] <= current_time:
                    new_process = remaining_processes.pop(0)
                    ready_queue.append(new_process)
                    print(f"Processo {new_process['pid']} adicionado à fila de prontos no tempo {current_time}")

               
                for p in ready_queue:
                    p['waiting_time'] += 1

            print(f"Processo {process['pid']} executado por {execution_time} unidades de tempo. Tempo atual: {current_time}")
 
            if process['remaining_time'] > 0:
                ready_queue.append(process)
                print(f"Processo {process['pid']} volta para a fila de prontos. Tempo restante: {process['remaining_time']}")
            else:
                
                turnaround_time = current_time - process['arrival_time']
                turnaround_times.append(turnaround_time)
                print(f"Processo {process['pid']} concluído. Tempo de término: {current_time}, Turnaround: {turnaround_time}")
        else:
           
            if remaining_processes:
                current_time = remaining_processes[0]['arrival_time']
                print(f"Nenhum processo na fila de prontos. Avançando o tempo para {current_time}")

    
    avg_turnaround = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
    return {'algorithm': 'Round Robin', 'avg_turnaround': avg_turnaround}


if __name__ == '__main__':
    app.run(debug=True)