def fifo_scheduler(processes):
    if not processes:
        return {'algorithm': 'FIFO', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    sorted_processes = sorted(processes, key=lambda x: (x['arrival_time'], x['pid']))
    current_time = 0
    turnaround_times = []
    executed = {}
    waiting = {}
    overhead = {}

    for process in sorted_processes:
        executed[process['pid']] = []
        waiting[process['pid']] = []
        overhead[process['pid']] = []

        if current_time < process['arrival_time']:
            for t in range(current_time, process['arrival_time']):
                waiting[process['pid']].append(t)
            current_time = process['arrival_time']

        for t in range(process['execution_time']):
            executed[process['pid']].append(current_time + t)
        
        turnaround_times.append(current_time + process['execution_time'] - process['arrival_time'])
        current_time += process['execution_time']

    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    return {'algorithm': 'FIFO', 'avg_turnaround': avg_turnaround, 'total_time': current_time, 'executed': executed, 'waiting': waiting, 'overhead': overhead}


def sjf_scheduler(processes):
    if not processes:
        return {'algorithm': 'SJF', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    sorted_processes = sorted(processes, key=lambda x: (x['arrival_time'], x['execution_time']))
    current_time = 0
    turnaround_times = []
    executed = {}
    waiting = {}
    overhead = {}
    ready_queue = []

    while sorted_processes or ready_queue:
        while sorted_processes and sorted_processes[0]['arrival_time'] <= current_time:
            process = sorted_processes.pop(0)
            ready_queue.append(process)
            executed[process['pid']] = []
            waiting[process['pid']] = []
            overhead[process['pid']] = []

        if ready_queue:
            ready_queue.sort(key=lambda x: x['execution_time'])
            process = ready_queue.pop(0)
            for t in range(process['execution_time']):
                executed[process['pid']].append(current_time + t)
            turnaround_times.append(current_time + process['execution_time'] - process['arrival_time'])
            current_time += process['execution_time']
        else:
            if sorted_processes:
                current_time = sorted_processes[0]['arrival_time']

    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    return {'algorithm': 'SJF', 'avg_turnaround': avg_turnaround, 'total_time': current_time, 'executed': executed, 'waiting': waiting, 'overhead': overhead}

def round_robin_scheduler(processes, quantum, overhead):
    if not processes:
        return {'algorithm': 'Round Robin', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    for process in processes:
        process['remaining_time'] = process['execution_time']
        process['waiting_time'] = 0  

    current_time = 0
    turnaround_times = []
    executed = {}
    waiting = {}
    overhead_time = {}
    ready_queue = []
    remaining_processes = sorted(processes, key=lambda x: (x['arrival_time'], x['pid']))  

    for process in remaining_processes:
        pid = process['pid']
        executed[pid] = []
        waiting[pid] = []
        overhead_time[pid] = []

    while remaining_processes or ready_queue:
        for p in ready_queue:
            if p['remaining_time'] > 0 and current_time not in executed[p['pid']]:
                waiting[p['pid']].append(current_time)  # Registra espera corretamente

        while remaining_processes and remaining_processes[0]['arrival_time'] <= current_time:
            process = remaining_processes.pop(0)
            ready_queue.append(process)
            print(f"Processo {process['pid']} adicionado à fila de prontos no tempo {current_time}")

        if ready_queue:
            ready_queue.sort(key=lambda x: -x['waiting_time'])  
            process = ready_queue.pop(0)  
            pid = process['pid']
            execution_time = min(quantum, process['remaining_time'])

            for _ in range(execution_time):
                executed[pid].append(current_time)
                if current_time in waiting[pid]:
                    waiting[pid].remove(current_time)
                current_time += 1
                process['remaining_time'] -= 1

                while remaining_processes and remaining_processes[0]['arrival_time'] <= current_time:
                    new_process = remaining_processes.pop(0)
                    ready_queue.append(new_process)
                    print(f"Processo {new_process['pid']} adicionado à fila de prontos no tempo {current_time}")

                for p in ready_queue:
                    p['waiting_time'] += 1
                    waiting[p['pid']].append(current_time)  # Adiciona tempo de espera corretamente

            print(f"Processo {process['pid']} executado por {execution_time} unidades de tempo. Tempo atual: {current_time}")
 
            if process['remaining_time'] > 0:
                for _ in range(overhead):
                    overhead_time[pid].append(current_time)
                    current_time += 1
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
    return {'algorithm': 'Round Robin', 'avg_turnaround': avg_turnaround, 'total_time': current_time, 'executed': executed, 'waiting': waiting, 'overhead': overhead_time}


def edf_scheduler(processes, quantum, overhead):
    if not processes:
        return {'algorithm': 'EDF', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    sorted_processes = sorted(processes, key=lambda x: (x['arrival_time'], x['deadline'], x['pid']))
    current_time = 0
    turnaround_times = []
    executed = {}
    waiting = {}
    overhead_time = {}
    ready_queue = []

    for process in sorted_processes:
        pid = process['pid']
        executed[pid] = []
        waiting[pid] = []
        overhead_time[pid] = []

    while sorted_processes or ready_queue:
        while sorted_processes and sorted_processes[0]['arrival_time'] <= current_time:
            ready_queue.append(sorted_processes.pop(0))
            ready_queue.sort(key=lambda x: x['deadline'])

        if ready_queue:
            process = ready_queue.pop(0)
            pid = process['pid']
            execution_time = min(process['execution_time'], quantum)
            
            for _ in range(execution_time):
                executed[pid].append(current_time)
                current_time += 1
                process['execution_time'] -= 1
                
            if process['execution_time'] > 0:
                for _ in range(overhead):
                    overhead_time[pid].append(current_time)
                    current_time += 1
                ready_queue.append(process)
                ready_queue.sort(key=lambda x: x['deadline'])
            else:
                turnaround_times.append(current_time - process['arrival_time'])
        
        else:
            if sorted_processes:
                current_time = sorted_processes[0]['arrival_time']

    avg_turnaround = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
    return {'algorithm': 'EDF', 'avg_turnaround': avg_turnaround, 'total_time': current_time, 'executed': executed, 'waiting': waiting, 'overhead': overhead_time}
