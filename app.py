from flask import Flask, jsonify, request, render_template

app = Flask (__name__)
customersList = [{

		"id"   : 1,
		"name" : "Nat",
		"lang" : "javaScript" 
	},
	{
		"id"   : 2,
		"name" : "Joaquin",
		"lang" : "CSharp" 
	},
	{
		"id"   : 3,
		"name" : "Harbor",
		"lang" : "Assembly" 
	},
	{
		"id"   : 4,
		"name" : "Philip",
		"lang" : "c++" 
	}
]

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/customersList', methods=['GET'])
def home():
	return jsonify (customersList), 200

@app.route('/enviar.html', methods = ['GET'])
def enviar():
	return jsonify("Dados enviados com sucesso!"), 200 # ORGANIZAR TODO
    #return render_template('index.html')

@app.route('/customersList/<string:name>', methods=['GET'])
def customerPerName(name):
	customerNames = []
	for customer in customersList:
		if customer['name'] == name:
			customerNames += customer
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
	dado = request.get_json(True, True, True)
	customersList.append(dado) #verificar se registro já existe
	return jsonify(customersList), 201

@app.route('/customersList/<int:id>', methods=['DELETE'])
def deleteCustomer(id):
	# realizar deleção lógica
	del customersList[id-1]
	return jsonify(customersList), 200

if __name__ == '__main__':
	app.run(debug = True, host = '127.0.0.1')

	