from flask import Flask, jsonify, request

app = Flask (__name__)


customersList = [
	{
		'id'   : 1,
		'name' : 'Miranda',
		'lang' : 'pitao'
	},
	{
		'id'   : 2,
		'name' : 'Joaquin',
		'lang' : 'CSharp' 
	},
	{
		'id'   : 3,
		'name' : 'Harbor',
		'lang' : 'Assembly' 
	},
	{
		'id'   : 4,
		'name' : 'Philip',
		'lang' : 'c++' 
	}
]

@app.route('/customersList', methods=['GET'])
def home():
	return jsonify(customersList), 200

@app.route('/customersList/<string:name>', methods=['GET'])
def customerPerName(name):
	customerNames = [customer for customer in customersList if customer['name'] == name]
	if customerNames == []:
		return jsonify ('Nenhum nome encontrado'), 401
	return jsonify(customerNames), 200

@app.route('/customersList/<int:id>', methods=['GET'])
def customerPerId(id):
	for customer in customersList:
		if customer['id'] == id:
			return jsonify (customer), 200
	return jsonify ('Nenhum Id encontrado'), 401


@app.route('/customersList', methods=['POST'])
def saveCustomer():
	data = request.get_json()
	customersList.append(data)
	return jsonify(data), 201

if __name__ == '__main__':
	app.run(debug = True)