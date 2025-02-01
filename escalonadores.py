def fifo_scheduler(processes):
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

def sjf_scheduler(processes):
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

def round_robin_scheduler(processes, quantum):
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

def edf_scheduler(processes, quantum, overhead):
    if not processes:
        return {'algorithm': 'EDF', 'avg_turnaround': 0, 'message': 'Nenhum processo para escalonar.'}

    sorted_processes = sorted(processes, key=lambda x: (x['arrival_time'], x['deadline']))

    current_time = 0
    turnaround_times = []
    ready_queue = []
    process_completion = {}

    while sorted_processes or ready_queue:
        while sorted_processes and sorted_processes[0]['arrival_time'] <= current_time:
            ready_queue.append(sorted_processes.pop(0))
            ready_queue.sort(key=lambda x: x['deadline'])

        if ready_queue:
            process = ready_queue.pop(0)
            execution_time = min(process['execution_time'], quantum)
            
            current_time += execution_time  # Executa por um quantum ou até terminar
            process['execution_time'] -= execution_time
            
            if process['execution_time'] > 0:
                current_time += overhead  # Adiciona sobrecarga ao trocar de processo
                ready_queue.append(process)  # Processo volta à fila se não terminou
            else:
                completion_time = current_time + overhead
                process_completion[process['pid']] = completion_time
                turnaround_times.append(completion_time - process['arrival_time'])
                
        else:
            if sorted_processes:
                current_time = sorted_processes[0]['arrival_time']

    avg_turnaround = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
    return {'algorithm': 'EDF', 'avg_turnaround': avg_turnaround, 'completion_times': process_completion}