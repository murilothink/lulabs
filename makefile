# Variáveis
DOCKER_COMPOSE = docker-compose
APP_SERVICE = app
DB_SERVICE = db
PYTHON = python

# Rodar o projeto
run:
	$(DOCKER_COMPOSE) up --build

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
