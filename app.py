from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('tarefas.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, concluida BOOLEAN NOT NULL CHECK (concluida IN (0, 1)))')
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tarefas', methods=['GET'])
def get_tarefas():
    conn = get_db_connection()
    tarefas = conn.execute('SELECT * FROM tarefas').fetchall()
    conn.close()
    return jsonify([dict(tarefa) for tarefa in tarefas])

@app.route('/tarefas', methods=['POST'])
def add_tarefa():
    nova_tarefa = request.get_json()
    titulo = nova_tarefa['titulo']
    conn = get_db_connection()
    conn.execute('INSERT INTO tarefas (titulo, concluida) VALUES (?, ?)', (titulo, 0))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Tarefa adicionada com sucesso!'})

# ESTA É A ROTA DE EXCLUSÃO, E ELA DEVE ESTAR AQUI!
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Tarefa excluída com sucesso!'})

if __name__ == '__main__':
    create_table()
    app.run(debug=True)