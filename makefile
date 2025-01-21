# Variáveis
DOCKER_COMPOSE = docker compose
APP_SERVICE = app
DB_SERVICE = db
PYTHON = python

# Alvo padrão (ajuda)
help:
	@echo "Comandos disponíveis:"
	@echo "  make install-docker      - Instala Docker e Docker Compose"
	@echo "  make run                 - Constrói e inicia os serviços"
	@echo "  make stop                - Para os serviços"
	@echo "  make bash                - Acessa o container da aplicação"
	@echo "  make install             - Instala dependências dentro do container"
	@echo "  make migrations          - Cria migrations do banco de dados"
	@echo "  make upgrade             - Aplica migrations no banco de dados"
	@echo "  make clean               - Remove containers, volumes e imagens órfãs"
	@echo "  make reset-db            - Reinicia o banco de dados"
	@echo "  make logs                - Exibe os logs do container da aplicação"
	@echo "  make test                - Executa os testes dentro do container"

# Instalação do Docker e Docker Compose
install-docker:
	@echo "Atualizando repositórios..."
	sudo apt update
	@echo "Instalando Docker..."
	sudo apt install -y docker.io
	@echo "Adicionando o usuário ao grupo Docker..."
	sudo usermod -aG docker $USER
	@echo "Instalando Docker Compose Plugin..."
	sudo apt install -y docker-compose-plugin
	@echo "Docker e Docker Compose instalados com sucesso!"
	@echo "Reinicie sua sessão ou execute 'newgrp docker' para aplicar as mudanças."

# Rodar o projeto
run:
	$(DOCKER_COMPOSE) up --build -d

# Parar os containers
stop:
	$(DOCKER_COMPOSE) down

# Acessar o container da aplicação
bash:
	$(DOCKER_COMPOSE) exec $(APP_SERVICE) bash

# Instalar dependências
install:
	$(DOCKER_COMPOSE) exec $(APP_SERVICE) pip install -r requirements.txt

# Criar migrations do banco de dados
migrations:
	$(DOCKER_COMPOSE) exec $(APP_SERVICE) flask db init
	$(DOCKER_COMPOSE) exec $(APP_SERVICE) flask db migrate -m "Initial migration"

# Aplicar migrations no banco
upgrade:
	$(DOCKER_COMPOSE) exec $(APP_SERVICE) flask db upgrade

# Limpar containers, volumes e imagens
clean:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
	docker rmi -f $$(docker images -f "dangling=true" -q) || true

# Reiniciar o banco de dados
reset-db: stop clean run upgrade

# Ver logs do container da aplicação
logs:
	$(DOCKER_COMPOSE) logs -f $(APP_SERVICE)

# Testar a aplicação
test:
	$(DOCKER_COMPOSE) exec $(APP_SERVICE) $(PYTHON) -m unittest discover -s tests
