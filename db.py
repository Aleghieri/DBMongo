from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient

# Parte 1 - Banco de Dados Relacional com SQLAlchemy

# Conexão com o banco de dados SQLite
engine = create_engine('sqlite:///banco_relacional.db')
Base = declarative_base(bind=engine)

# Definição das classes Cliente e Conta
class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)

class Conta(Base):
    __tablename__ = 'conta'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    numero = Column(String)
    saldo = Column(Integer)

# Criação das tabelas no banco de dados
Base.metadata.create_all()

# Inserção de dados no banco de dados
Session = sessionmaker(bind=engine)
session = Session()

cliente1 = Cliente(nome='João', email='joao@example.com')
cliente2 = Cliente(nome='Maria', email='maria@example.com')

conta1 = Conta(cliente_id=1, numero='123', saldo=1000)
conta2 = Conta(cliente_id=2, numero='456', saldo=2000)

session.add_all([cliente1, cliente2, conta1, conta2])
session.commit()

# Recuperação de dados do banco de dados
clientes = session.query(Cliente).all()
contas = session.query(Conta).all()

print("Clientes:")
for cliente in clientes:
    print(cliente.id, cliente.nome, cliente.email)

print("Contas:")
for conta in contas:
    print(conta.id, conta.numero, conta.saldo)


# Parte 2 - Banco de Dados NoSQL com PyMongo

# Conexão com o banco de dados MongoDB
client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client['nome_do_banco_de_dados']
bank_collection = db['bank']

# Inserção de documentos no banco de dados
cliente1 = {
    'nome': 'João',
    'email': 'joao@example.com',
    'contas': [
        {
            'numero': '123',
            'saldo': 1000
        }
    ]
}

cliente2 = {
    'nome': 'Maria',
    'email': 'maria@example.com',
    'contas': [
        {
            'numero': '456',
            'saldo': 2000
        }
    ]
}

bank_collection.insert_many([cliente1, cliente2])

# Recuperação de informações do banco de dados
clientes = bank_collection.find()

print("Clientes:")
for cliente in clientes:
    print(cliente['nome'], cliente['email'])

print("Contas:")
contas = bank_collection.find({}, {'contas': 1})

for cliente in contas:
    for conta in cliente['contas']:
        print(conta['numero'], conta['saldo'])
