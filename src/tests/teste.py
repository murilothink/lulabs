from sqlalchemy import create_engine, text

# Configuração do banco de dados
DATABASE_URI = "postgresql://user:password@localhost:5432/lulabs_db"

# Criar o engine e conectar-se ao banco
engine = create_engine(DATABASE_URI)

try:
    with engine.connect() as conn:
        print("Conectado ao banco de dados!")
        # Executar um comando SQL para verificar a conexão
        result = conn.execute(text("SELECT version();"))
        for row in result:
            print(f"Versão do PostgreSQL: {row[0]}")
except Exception as e:
    print(f"Erro ao conectar ao banco: {e}")
