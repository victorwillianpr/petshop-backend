from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Configura o CORS para permitir todas as origens

CONNECTION_STRING = #########
DATABASE_NAME = "petshop"
COLLECTION_AGENDAMENTOS = "agendamentos"
COLLECTION_TUTORES = "tutores"
COLLECTION_PETS = "pets"
COLLECTION_PROFISSIONAIS = "profissionais"
COLLECTION_SERVIÇOS = "serviços"

# Conecta ao MongoDB Atlas
client = MongoClient(CONNECTION_STRING)
db = client[DATABASE_NAME]
collectionAgendamentos = db[COLLECTION_AGENDAMENTOS]
collectionTutores = db[COLLECTION_TUTORES]
collectionPets = db[COLLECTION_PETS]
collectionProfissionais = db[COLLECTION_PROFISSIONAIS]
collectionServicos = db[COLLECTION_SERVIÇOS]

@app.route('/')
def index():
    return "Bem-vindo ao backend Flask!"

@app.route('/api/agendamentos', methods=['POST'])
def create_agendamento():
    try:
        agendamento_data = request.json
        required_fields = ['data', 'hora', 'servico', 'profissional', 'pet', 'tutor']
        if not all(field in agendamento_data for field in required_fields):
            return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

        result = collectionAgendamentos.insert_one(agendamento_data)
        return jsonify({'message': 'Agendamento criado com sucesso!', 'id': str(result.inserted_id)}), 201

    except PyMongoError as e:
        return jsonify({'error': f'Erro ao inserir o agendamento: {e}'}), 500

def remove_objectid(doc):
    if '_id' in doc:
        del doc['_id']
    return doc

@app.route('/api/agendamentos/futuros', methods=['GET'])
def get_agendamentos_futuros():
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        agendamentos = list(collectionAgendamentos.find({"data": {"$gte": today}}))
        
        # Adicionar o nome do pet
        for agendamento in agendamentos:
            pet_id = agendamento.get('pet')
            if pet_id:
                pet = collectionPets.find_one({"_id": pet_id}, {"_id": 0, "nome": 1})
                agendamento['petNome'] = pet['nome'] if pet else 'Desconhecido'
        
        agendamentos = [remove_objectid(agendamento) for agendamento in agendamentos]
        return jsonify(agendamentos), 200
    except PyMongoError as e:
        return jsonify({'error': f'Erro ao buscar agendamentos futuros: {e}'}), 500


@app.route('/api/agendamentos/realizados', methods=['GET'])
def get_agendamentos_realizados():
    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        agendamentos = list(collectionAgendamentos.find({"data": {"$lte": yesterday}}))
        agendamentos = [remove_objectid(agendamento) for agendamento in agendamentos]
        return jsonify(agendamentos), 200
    except PyMongoError as e:
        return jsonify({'error': f'Erro ao buscar agendamentos realizados: {e}'}), 500

@app.route('/api/tutores', methods=['GET'])
def get_tutores():
    try:
        tutores = list(collectionTutores.find({}, {"_id": 0, "nome": 1}))
        return jsonify(tutores), 200
    except PyMongoError as e:
        return jsonify({'error': f'Erro ao buscar tutores: {e}'}), 500

@app.route('/api/tutores', methods=['POST'])
def create_tutor():
    try:
        tutor_data = request.json
        required_fields = ['nome', 'cpf', 'email']
        if not all(field in tutor_data for field in required_fields):
            return jsonify({'error': 'Todos os campos obrigatórios devem ser preenchidos!'}), 400

        result = collectionTutores.insert_one(tutor_data)
        return jsonify({'message': 'Tutor cadastrado com sucesso!', 'id': str(result.inserted_id)}), 201

    except PyMongoError as e:
        return jsonify({'error': f'Erro ao cadastrar o tutor: {e}'}), 500

@app.route('/api/pets', methods=['POST'])
def create_pet():
    try:
        pet_data = request.json
        required_fields = ['nome', 'raca', 'tutor']
        if not all(field in pet_data for field in required_fields):
            return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

        result = collectionPets.insert_one(pet_data)
        return jsonify({'message': 'Pet cadastrado com sucesso!', 'id': str(result.inserted_id)}), 201

    except PyMongoError as e:
        return jsonify({'error': f'Erro ao cadastrar o pet: {e}'}), 500

@app.route('/api/pets', methods=['GET'])
def get_pets():
    try:
        tutores = list(collectionPets.find({}, {"_id": 0, "nome": 1}))
        return jsonify(tutores), 200
    except PyMongoError as e:
        return jsonify({'error': f'Erro ao buscar tutores: {e}'}), 500

@app.route('/api/profissionais', methods=['POST'])
def create_profissional():
    try:
        profissional_data = request.json
        required_fields = ['nome', 'email', 'cpf']
        if not all(field in profissional_data for field in required_fields):
            return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

        result = collectionProfissionais.insert_one(profissional_data)
        return jsonify({'message': 'Profissional cadastrado com sucesso!', 'id': str(result.inserted_id)}), 201

    except PyMongoError as e:
        return jsonify({'error': f'Erro ao cadastrar o profissional: {e}'}), 500

@app.route('/api/profissionais', methods=['GET'])
def get_profissionais():
    try:
        tutores = list(collectionProfissionais.find({}, {"_id": 0, "nome": 1}))
        return jsonify(tutores), 200
    except PyMongoError as e:
        return jsonify({'error': f'Erro ao buscar tutores: {e}'}), 500

@app.route('/api/servicos', methods=['POST'])
def create_servico():
    try:
        servico_data = request.json
        required_fields = ['tipo', 'preco']
        if not all(field in servico_data for field in required_fields):
            return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

        result = collectionServicos.insert_one(servico_data)
        return jsonify({'message': 'Serviço cadastrado com sucesso!', 'id': str(result.inserted_id)}), 201

    except PyMongoError as e:
        return jsonify({'error': f'Erro ao cadastrar o serviço: {e}'}), 500

@app.route('/api/servicos', methods=['GET'])
def get_servicos():
    try:
        servicos = list(collectionServicos.find({}, {"_id": 0, "tipo": 1, "preco": 1}))
        return jsonify(servicos), 200
    except PyMongoError as e:
        return jsonify({'error': f'Erro ao buscar serviços: {e}'}), 500

@app.route('/api/consultas', methods=['POST'])
def create_consulta():
    try:
        consulta_data = request.json
        required_fields = ['data', 'retorno', 'sintomas', 'diagnostico', 'tratamento', 'petNome']
        if not all(field in consulta_data for field in required_fields):
            return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

        result = db.consultas.insert_one(consulta_data)
        return jsonify({'message': 'Consulta criada com sucesso!', 'id': str(result.inserted_id)}), 201

    except PyMongoError as e:
        return jsonify({'error': f'Erro ao inserir a consulta: {e}'}), 500

@app.route('/api/consultas', methods=['GET'])
def get_consultas():
    try:
        consultas = list(db.consultas.find({}, {"_id": 0}))
        return jsonify(consultas), 200
    except PyMongoError as e:
        return jsonify({'error': f'Erro ao buscar consultas: {e}'}), 500


if __name__ == "__main__":
    app.run(debug=True)
