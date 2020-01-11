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
    return render_template('index.html')

@app.route('/allCustomers', methods=['GET'])
def getAllCustomers():
	allCustomers = CustomerModel.query.all()
	customerSchema = CustomerSchema(many=True)
	outPut = customerSchema.dump(allCustomers)
	return jsonify({'customers':outPut}), 200

@app.route('/allCustomers/<string:namePassed>', methods=['GET'])
def getCustomerPerName(namePassed):
	#specificCustomer = CustomerModel.query.filter(CustomerModel.name == namePassed)
	specificCustomer = CustomerModel.query.filter(CustomerModel.name.like("%" + str(namePassed) + "%"), CustomerModel.historic == False)
	customerSchema = CustomerSchema(many=True)
	outPut = customerSchema.dump(specificCustomer)
	return jsonify({'customer':outPut}), 200

@app.route('/sendRegistry', methods=['POST'])
def postCustomer():
	engine = create_engine(config.connectionString)
	Session = sessionmaker(bind=engine)
	session = Session()
	data = request.get_json(True, True, True)
	customerToAdd = CustomerModel(name = data['name'], birthDay = data['birthDay'], generalRegistry = data['generalRegistry'], address = data['address'], phoneNumber = data['phoneNumber'], historic = False) # Acabou de criar não é historico
	session.add(customerToAdd)
	session.commit()
	return jsonify(customerToAdd.name), 201


if __name__ == '__main__':
	app.run(debug = True, host = '127.0.0.1')

	