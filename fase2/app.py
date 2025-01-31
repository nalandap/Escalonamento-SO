from flask import Flask, render_template, request, jsonify
from .substituicao import fifo_substituicao, lru_substituicao
from .memoria import RAM, Disco

app = Flask(__name__)

# Inicializa a memória RAM e o Disco
ram = RAM(capacidade=50)  # 50 páginas de 4 KB cada (200 KB)
disco = Disco()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adicionar_processo', methods=['POST'])
def adicionar_processo():
    data = request.json
    paginas = int(data['paginas'])
    # Adiciona o processo à memória (RAM ou Disco)
    # Implementar lógica aqui
    return jsonify({'message': 'Processo adicionado com sucesso!'})

@app.route('/executar_substituicao', methods=['POST'])
def executar_substituicao():
    algoritmo = request.json['algoritmo']
    if algoritmo == 'FIFO':
        resultado = fifo_substituicao(ram, disco)
    elif algoritmo == 'LRU':
        resultado = lru_substituicao(ram, disco)
    else:
        return jsonify({'error': 'Algoritmo desconhecido'}), 400
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)