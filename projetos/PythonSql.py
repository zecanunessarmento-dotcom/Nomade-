import pyodbc 

dados_Conexao = (
    "Driver={SQL SERVER};"
    "Server=DESKTOP-E7UKFM4;"
    "Database=PythonSQL;"
)

conexao = pyodbc.connect(dados_Conexao)
print("Conexão Bem sucedida")

cursor = conexao.cursor()


id = 3
cliente = "Lira Python"
produto = "Carro"
data = "25/08/2021"
preço = 5000
quantidade = 1

comando = f"""INSERT INTO Vendas(id_venda, cliente, produto, data_venda, preco, quantidade)
VALUES
    ({id}, '{cliente}' , '{produto}' , '{data}' , {preço} , {quantidade})"""

cursor.execute(comando)
cursor.commit()