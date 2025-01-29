from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dados dos processos (simulando um banco de dados)
processes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_process', methods=['POST'])
def add_process():
    data = request.json
    process = {
        'pid': len(processes) + 1,
        'arrival_time': int(data['arrival_time']),
        'execution_time': int(data['execution_time']),
        'deadline': int(data['deadline']),
        'quantum': int(data['quantum']),
        'overhead': int(data['overhead'])
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
        result = round_robin_scheduler()
    elif algorithm == 'EDF':
        result = edf_scheduler()

    return jsonify(result)

def fifo_scheduler():
    # Implementação do FIFO
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
    # Implementação do SJF
    sorted_processes = sorted(processes, key=lambda x: (x['arrival_time'], x['execution_time']))
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
    return {'algorithm': 'SJF', 'avg_turnaround': avg_turnaround}

# Implementações para Round Robin e EDF podem ser adicionadas aqui

if __name__ == '__main__':
    app.run(debug=True)