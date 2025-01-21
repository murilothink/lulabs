# Define os dados
dados = [
    {
        "id_usuario": "0000000001",
        "nome": "Medeiros",
        "id_pedido": "00000012345",
        "id_produto": "00000000111",
        "valor_produto": "256.24",
        "data_compra": "20201201",
    },
    {
        "id_usuario": "0000000002",
        "nome": "Zarelli",
        "id_pedido": "00000001230",
        "id_produto": "00000000111",
        "valor_produto": "512.24",
        "data_compra": "20211201",
    },
    {
        "id_usuario": "0000000002",
        "nome": "Zarelli",
        "id_pedido": "00000001230",
        "id_produto": "00000000122",
        "valor_produto": "512.24",
        "data_compra": "20211201",
    },
    {
        "id_usuario": "0000000001",
        "nome": "Medeiros",
        "id_pedido": "00000012345",
        "id_produto": "00000000122",
        "valor_produto": "256.24",
        "data_compra": "20201201",
    },
]

# Gera o arquivo
with open("dados_exemplo.txt", "w") as arquivo:
    for item in dados:
        linha = (
            f"{item['id_usuario']:<10}"
            f"{item['nome']:<45}"
            f"{item['id_pedido']:<10}"
            f"{item['id_produto']:<10}"
            f"{float(item['valor_produto']):>12.2f}"
            f"{item['data_compra']:<8}"
        )
        arquivo.write(linha + "\n")

print("Arquivo gerado com sucesso: dados_exemplo.txt")
