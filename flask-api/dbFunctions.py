import MySQLdb
import MySQLdb.cursors

# Método para criar Conexão
def makeConnection(retornaDict = False):
	dbConfig = ConfigDataBase()
	if retornaDict:
		return MySQLdb.connect(host=dbConfig["host"],user=dbConfig["user"],passwd=dbConfig["passwd"],db=dbConfig["db"],cursorclass=MySQLdb.cursors.DictCursor)
	else:
		return MySQLdb.connect(host=dbConfig["host"],user=dbConfig["user"],passwd=dbConfig["passwd"],db=dbConfig["db"])



def ConfigDataBase():
	return { 
		"host": "registers", 
		"user": "root", 
		"passwd": "root", 
		"db": "projSympla"
	}