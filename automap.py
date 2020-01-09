from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, and_
import datetime
import json
import config


connection_str = 'mysql+pymysql://' + config.user+ ':'+ config.password + '@' + config.host+ ':' + config.port + '/' + config.database

Base = declarative_base()
engine = create_engine(connection_str, encoding="utf8", echo = True) #echo para dar os logs do banco em real-time
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Customer(Base):
    __tablename__ = 'customersTable' #nome da tabela dele no banco
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthDay = Column(String)
    generalRegistry = Column(String)
    address = Column(String)
    phoneNumber = Column(String)
    historic = Column(Boolean)
    
    def __repr__(self):
        return "<Customer(name=" + self.name + ", birthDay=" + self.birthDay + ", generalRegistry=" + self.generalRegistry + ", address=" + self.address + ", phoneNumber=" + self.phoneNumber + ", historic=" + self.historic + ">"
        
def getAllCustomers(name = '', includeHistorics = False):
    # sei que algo deste tipo pode acarretar em uma sobrecarga do banco, se houver muitos registros.
    if includeHistorics:
        allCustomers = session.query(Customer).filter(Customer.name.like('%' + str(name) + '%')).all() # modifiquei, testar TODO
    else:
        allCustomers = session.query(Customer).filter(Customer.name.like('%' + str(name) + '%'),Customer.historic == False).all()
    return allCustomers

def getSpecificCustomer(name = '', justOne = False):
    if justOne: # busca por nomes que nao sao historicos
        especificCustomer = session.query(Customer).filter(Customer.name == str(name), Customer.historic == False).first()
    else:
        especificCustomer = session.query(Customer).filter(Customer.name.like('%' + str(name) + '%'), Customer.historic == False).all()
    return especificCustomer

def removeCustomer(nome = ''):
    if nome is None:
        return False
    toBeDeleted = getSpecificCustomer(nome, True)
    ch = toBeDeleted #copia do objeto para ser reinserido com historic True
    session.delete(toBeDeleted)
    session.commit()
    add = Customer( # deleção lógica
        id = ch.id, 
        name = ch.name, 
        birthDay = ch.birthDay, 
        generalRegistry = ch.generalRegistry, 
        address = ch.address, 
        phoneNumber = ch.phoneNumber,
        historic = True)
    session.add(add)
    session.commit()
    return True
def addCustomer(name="", birthDay=format(datetime.datetime.now()), generalRegistry="", address="", phoneNumber="", historic = False):
    customerToAdd = Customer(name="FALSO de Triste", birthDay=format(datetime.datetime.now()), generalRegistry= "Falso.333", address="2-Rua Dinorá Gonsalves - BH - MG", phoneNumber="22-9-12332-333", historic = False)
    session.add(customerToAdd)
    session.commit()
# def removeCustomer(toBeDeleted = None):
#     if toBeDeleted == None:
#         return
#     session.query(Customer).delete(toBeDeleted)
#     session.commit()
#     return 'Deletado'




#customer = Customer(name="FALSO de Triste", birthDay=format(datetime.datetime.now()), generalRegistry= "Falso.333", address="2-Rua Dinorá Gonsalves - BH - MG", phoneNumber="22-9-12332-333", historic = False)
customer = getSpecificCustomer('Juan Coitado de Triste', True)
print(customer.name, customer.id)
#removeCustomer('Juan Coitado de Triste')


#customer = getAllCustomers('FALSO de Triste', True)
#print (customer.name)
# for c in customer:
#     print(c.name)


#session.commit()

# allCl = getSpecificCustomer('N', True)
# print (allCl.name)
#allCl = getAllCustomers()
# ''''
# for c in allCl:
#     print(c.name)
# ''''