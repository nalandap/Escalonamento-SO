from flask import Flask, render_template, request, jsonify
from escalonadores import fifo_scheduler, sjf_scheduler, round_robin_scheduler, edf_scheduler
#from memoria import RAM, Disco
#from substituicao import fifo_substituicao, lru_substituicao

app = Flask(__name__)

processes = []
quantum = None
overhead = None

# Dados globais para a Fase 2 (Substituição de Páginas)
#ram = RAM(capacidade=50)  
#disco = Disco()

# Rotas da Fase 1
@app.route('/')
def index():
    return render_template('index_fase1.html', quantum=quantum, overhead=overhead, process_list=processes)

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
        result = fifo_scheduler(processes)
    elif algorithm == 'SJF':
        result = sjf_scheduler(processes)
    elif algorithm == 'Round Robin':
        if quantum is None:
            return jsonify({'error': 'Quantum não definido'}), 400
        result = round_robin_scheduler(processes)
    elif algorithm == 'EDF':
        result = edf_scheduler(processes, quantum, overhead)
    else:
        return jsonify({'error': 'Algoritmo desconhecido'}), 400

    return jsonify(result)



    # Rotas da Fase 2
    #@app.route('/fase2')
    #def fase2():
        #return render_template('index_fase2.html')

    #@app.route('/fase2/adicionar_pagina', methods=['POST'])
    #def adicionar_pagina():
        #data = request.json
        #nova_pagina = {
            #'id': len(ram.paginas) + len(disco.paginas) + 1,
            #'#ultimo_acesso': data.get('ultimo_acesso', 0)
        #}
        #algoritmo = data.get('algoritmo', 'FIFO')

        #if algoritmo == 'FIFO':
         #   resultado = fifo_substituicao(ram, disco, nova_pagina)
        #elif algoritmo == 'LRU':
         #   resultado = lru_substituicao(ram, disco, nova_pagina)
       # else:
           # return jsonify({'error': 'Algoritmo desconhecido'}), 400

        #return jsonify({
            #'message': resultado,
           # 'ram': str(ram),
            #'disco': str(disco)p})
if __name__ == '__main__':
    app.run(debug=True)
