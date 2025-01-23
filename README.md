# Projeto Flask com Docker e PostgreSQL

Este projeto utiliza **Flask**, **Docker**, **PostgreSQL** e **Makefile** para criar uma API simples com endpoints de upload e consulta de dados.

---

## **Sumário**

1. [Requisitos](#requisitos)
2. [Configuração Inicial](#configuração-inicial)
3. [Comandos do Makefile](#comandos-do-makefile)
4. [Endpoints](#endpoints)
   - [Upload de Arquivo](#upload-de-arquivo)
   - [Consulta de Usuários](#consulta-de-usuários)
5. [Acessando o Banco de Dados](#acessando-o-banco-de-dados)
6. [Testando a Aplicação](#testando-a-aplicação)

---

## **Requisitos**

Certifique-se de ter as seguintes ferramentas instaladas:

- Docker
- Docker Compose (v2 ou superior)
- Make

---

## **Configuração Inicial**

1. Clone este repositório:
   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. Configura o ambiente e instala o Docker e Docker Compose:
   ```bash
   make setup
   ```

3. Instale o Docker e o Docker Compose (caso ainda não tenha):
   ```bash
   make install-docker
   ```

4. Inicie os serviços (Flask e PostgreSQL):
   ```bash
   make run
   ```

5. Verifique os logs para garantir que os serviços estão funcionando:
   ```bash
   make logs
   ```

---

## **Comandos do Makefile**

| Comando                | Descrição                                                                              |
|------------------------|----------------------------------------------------------------------------------------|
| `make setup`           | Configura o ambiente e dependência e Instala Docker e Docker Compose no sistema.       |
| `make install-docker`  | Instala Docker e Docker Compose no sistema.                                            |
| `make run`             | Constrói e inicia os serviços em background.                                           |
| `make stop`            | Para os serviços.                                                                      |
| `make bash`            | Abre um shell no container Flask.                                                      |
| `make install`         | Instala dependências dentro do container Flask.                                        |
| `make migrations`      | Cria as migrations do banco de dados.                                                  |
| `make upgrade`         | Aplica as migrations no banco de dados.                                                |
| `make clean`           | Remove containers, volumes e imagens órfãs.                                            |
| `make reset-db`        | Reinicia o banco de dados do zero.                                                     |
| `make logs`            | Exibe os logs do container Flask.                                                      |
| `make test`            | Executa os testes dentro do container Flask.                                           |
| `make fix-lint`        | Padronizar e organizar o código.                                           |
---

## **Endpoints**

### **Upload de Arquivo**

- **URL:** `/upload`
- **Método:** `POST`
- **Descrição:** Envia um arquivo para processar os dados de usuários e pedidos.
- **Exemplo de Uso:**

  ```bash
  curl -X POST -F "file=@/caminho/src/tests/seuarquivo.txt" http://localhost:5000/upload
  ```

- **Resposta de Sucesso:**
  ```json
  {
    "message": "File processed successfully",
    "data": [
      {
        "user_id": 1,
        "name": "Medeiros",
        "orders": [
          {
            "order_id": 12345,
            "total": "512.48",
            "date": "2020-12-01",
            "products": [
              { "product_id": 11, "value": 256.24 },
              { "product_id": 12, "value": 256.24 }
            ]
          }
        ]
      }
    ]
  }
  ```

### **Consulta de Usuários**

- **URL:** `/users`
- **Método:** `GET`
- **Descrição:** Retorna os dados de um ou todos os usuários processados.

- **Exemplo para Listar Todos os Usuários:**
  ```bash
  curl -X GET http://localhost:5000/users
  ```

- **Exemplo para Buscar um Usuário Específico:**
  ```bash
  curl -X GET "http://localhost:5000/users?user_id=70"
  ```


- **Resposta de Sucesso:**
  ```json
  {
    "name": "Palmer Prosacco",
    "orders": [
      {
        "date": "2021-11-13",
        "order_id": 749,
        "products": [
          {
            "product_id": 5,
            "value": 451.29
          },
          {
            "product_id": 2,
            "value": 1699.42
          },
          {
            "product_id": 3,
            "value": 559.47
          },
          {
            "product_id": 5,
            "value": 827.71
          }
        ],
        "total": "3537.89"
      },
      {
        "date": "2021-07-09",
        "order_id": 750,
        "products": [
          {
            "product_id": 4,
            "value": 1161.97
          },
          {
            "product_id": 4,
            "value": 335.14
          },
          {
            "product_id": 5,
            "value": 395.38
          },
          {
            "product_id": 3,
            "value": 343.43
          }
        ],
        "total": "2235.92"
      },
      {
        "date": "2021-04-07",
        "order_id": 751,
        "products": [
          {
            "product_id": 5,
            "value": 942.54
          },
          {
            "product_id": 3,
            "value": 648.2
          },
          {
            "product_id": 4,
            "value": 759
          },
          {
            "product_id": 4,
            "value": 1102.29
          }
        ],
        "total": "3452.03"
      },
      {
        "date": "2021-10-26",
        "order_id": 752,
        "products": [
          {
            "product_id": 4,
            "value": 1493.61
          },
          {
            "product_id": 1,
            "value": 1195.39
          },
          {
            "product_id": 7,
            "value": 509.31
          },
          {
            "product_id": 6,
            "value": 386.93
          }
        ],
        "total": "3585.24"
      },
      {
        "date": "2021-03-08",
        "order_id": 753,
        "products": [
          {
            "product_id": 3,
            "value": 1836.74
          },
          {
            "product_id": 3,
            "value": 1009.54
          },
          {
            "product_id": 4,
            "value": 618.79
          },
          {
            "product_id": 3,
            "value": 787.46
          }
        ],
        "total": "4252.53"
      },
      {
        "date": "2021-07-12",
        "order_id": 754,
        "products": [
          {
            "product_id": 3,
            "value": 97.99
          },
          {
            "product_id": 2,
            "value": 951.32
          },
          {
            "product_id": 2,
            "value": 1108.06
          },
          {
            "product_id": 6,
            "value": 1819.3
          }
        ],
        "total": "3976.67"
      },
      {
        "date": "2021-12-19",
        "order_id": 755,
        "products": [
          {
            "product_id": 1,
            "value": 901.93
          },
          {
            "product_id": 1,
            "value": 390.27
          },
          {
            "product_id": 4,
            "value": 1842.77
          },
          {
            "product_id": 6,
            "value": 887.2
          }
        ],
        "total": "4022.17"
      },
      {
        "date": "2021-10-02",
        "order_id": 756,
        "products": [
          {
            "product_id": 2,
            "value": 349.93
          },
          {
            "product_id": 3,
            "value": 1869.82
          },
          {
            "product_id": 4,
            "value": 752.4
          },
          {
            "product_id": 6,
            "value": 1643.41
          }
        ],
        "total": "4615.56"
      },
      {
        "date": "2021-11-23",
        "order_id": 757,
        "products": [
          {
            "product_id": 2,
            "value": 1300.18
          },
          {
            "product_id": 5,
            "value": 851.21
          },
          {
            "product_id": 4,
            "value": 1631.05
          },
          {
            "product_id": 4,
            "value": 1517.84
          }
        ],
        "total": "5300.28"
      },
      {
        "date": "2021-11-12",
        "order_id": 758,
        "products": [
          {
            "product_id": 4,
            "value": 518.33
          },
          {
            "product_id": 5,
            "value": 273.73
          },
          {
            "product_id": 6,
            "value": 1519.81
          },
          {
            "product_id": 0,
            "value": 1263.93
          }
        ],
        "total": "3575.80"
      }
    ],
    "user_id": 70
  }
  ```

---

- **Exemplo para Buscar uma Data Específica:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/users?date=2021-11-13"
  ```

## **Acessando o Banco de Dados**

### Via Docker
1. Verifique o nome do container PostgreSQL:
   ```bash
   docker ps
   ```

2. Acesse o terminal do PostgreSQL:
   ```bash
   docker exec -it postgres_db psql -U user -d lulabs_db
   ```

3. Execute comandos SQL no terminal `psql`:
   ```sql
   \l         -- Lista todos os bancos
   \c lulabs_db  -- Conecta ao banco "lulabs_db"
   \dt        -- Lista todas as tabelas
   SELECT * FROM users; -- Consulta dados da tabela "users"
   ```

4. Saia do terminal com:
   ```bash
   \q
   ```

### Via Cliente Local
Certifique-se de que o cliente PostgreSQL está instalado no seu sistema:

```bash
sudo apt install postgresql-client
```

Acesse o banco:
```bash
psql -h localhost -p 5432 -U user -d lulabs_db
```

---

## **Testando a Aplicação**

1. Execute os testes automatizados dentro do container Flask:
   ```bash
   make test
   ```

2. Verifique os resultados para garantir que tudo está funcionando corretamente.

---

Se precisar de mais detalhes ou suporte, entre em contato! 🚀

