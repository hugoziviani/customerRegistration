from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import config

app = Flask (__name__)

db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI']= config.connectionString


class CustomerModel(db.Model):
    __tablename__ = 'customersTable' #nome da tabela dele no banco
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birthDay = db.Column(db.String)
    generalRegistry = db.Column(db.String)
    address = db.Column(db.String)
    phoneNumber = db.Column(db.String)
    historic = db.Column(db.Boolean)
    
    def __repr__(self):
        return ("<Customer(name=" + self.name 
		+ ", birthDay=" + self.birthDay 
		+ ", generalRegistry=" + self.generalRegistry 
		+ ", address=" + self.address 
		+ ", phoneNumber=" + self.phoneNumber 
		+ ", historic=" + self.historic + ">")
class CustomerSchema(ma.ModelSchema):
	class Meta:
		model = CustomerModel


@app.route('/index.html')
def index():
	#não consegui relacionar a tempo o web-form com a API e o BD
	#seguirei tentando
    return render_template('index.html')

@app.route('/allCustomers', methods=['GET'])
def getAllCustomers():
	#aqui poderiamos limitar registros por data ou uma quantidade específica para não dar over no BD
	try:
		allCustomers = CustomerModel.query.all()
		customerSchema = CustomerSchema(many=True)
		outPut = customerSchema.dump(allCustomers)
		print ('Registros retornados com sucesso')
		return jsonify({'customers':outPut}), 200
	except:
		print ('Não foi possível retornar todos os registros')

@app.route('/allCustomers/<string:namePassed>', methods=['GET'])
def getCustomerPerName(namePassed):
	#busca por um nome específico proveniente da chamada da API
	try:
		specificCustomer = CustomerModel.query.filter(CustomerModel.name.like("%" + str(namePassed) + "%"), CustomerModel.historic == False)
		customerSchema = CustomerSchema(many=True)
		outPut = customerSchema.dump(specificCustomer)
		print ('Obj. retornado com sucesso')
		return jsonify({'customer':outPut}), 200
	except:	
		print ('localizar o registro, Obj. pode não  ser existente no banco')

@app.route('/sendRegistry', methods=['POST'])
def postCustomer():
	#adiciona um registro conforme o JSON vindo da requisição
	try:
		engine = create_engine(config.connectionString)
		Session = sessionmaker(bind=engine)
		session = Session()
		data = request.get_json()
		customerToAdd = CustomerModel(name = data['name'], birthDay = data['birthDay'], generalRegistry = data['generalRegistry'], address = data['address'], phoneNumber = data['phoneNumber'], historic = False) # Acabou de criar não é historico
		session.add(customerToAdd)
		session.commit()
		print ('Obj. adicionado ao banco com sucesso')
		return jsonify(data), 201
	except:
		#para isso poderia realizar verificação do registro no banco, a fim de evitar duplicatas
		print ('Não foi possivel adicionar Obj.')

@app.route('/<string:nameToDelete>', methods=['GET'])
def removeCustomer(nameToDelete):
	# realiza a deleção lógica, a fim de resguardar os dados no banco
	try:
		engine = create_engine(config.connectionString)
		Session = sessionmaker(bind=engine)
		session = Session()
		toBeDeleted = session.query(CustomerModel).filter(CustomerModel.name.like('%' + str(nameToDelete) + '%'), CustomerModel.historic == False).first()
		ch = toBeDeleted
		session.delete(toBeDeleted)
		session.commit()
		addCs = CustomerModel(id = ch.id, name = ch.name, birthDay = ch.birthDay, generalRegistry = ch.generalRegistry, address = ch.address, phoneNumber = ch.phoneNumber, historic = True)
		session.add(addCs)
		session.commit()
		customerSchema = CustomerSchema()
		outPut = customerSchema.dump(ch)
		print ('Deleção realizada com sucesso')
	except:
		print ('Não foi possivel realizar deleção, Obj. não existente no banco')
	return jsonify({'toBeDeleted': outPut }), 200

if __name__ == '__main__':
	app.run(debug = True, host = '127.0.0.1')

	