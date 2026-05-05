# Painel de Logística — API de Rastreamento

API backend para um sistema de logística e rastreamento de entregas urbanas. Clientes criam pedidos, entregadores recebem rotas e enviam pings de GPS, administradores gerenciam operações.

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Framework | FastAPI (Python 3.10) |
| ORM | SQLAlchemy 2.0 (async) |
| Banco de dados | PostgreSQL 16 |
| Driver async | asyncpg |
| Validação | Pydantic v2 |
| Autenticação | JWT (PyJWT) |
| Hash de senha | pwdlib + Argon2 |
| Rate limiting | slowapi |
| Containerização | Docker + Docker Compose |

---

## .ENV
```
API_VERSION=1.0.0
APP_NAME=Name_of_your_app

FASTAPI_ENV=development
DATABASE_DIALECT=postgresql+asyncpg
DATABASE_HOST=Your_db_host
DATABASE_PORT=Your_db_port
DATABASE_USERNAME=Your_db_username
DATABASE_PASSWORD=Your_db_password
DATABASE_NAME=Your_db_name
DEBUG_MODE=true
SECRET_KEY=Your_secret_key
ALGORITHM=Your_hash_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```





## Arquitetura

O projeto segue **Clean Architecture** com separação em camadas:

```
app/
├── auth/           # JWT, segurança, dependências de papéis
├── configs/        # Configurações de ambiente e banco
├── core/           # Exceções customizadas
├── models/         # Entidades SQLAlchemy (ORM)
├── repositories/   # Acesso ao banco de dados
├── schemas/        # Schemas Pydantic (entrada/saída)
├── services/       # Regras de negócio
└── routers/v1/     # Endpoints da API
```

**Padrões utilizados:** Service Pattern · Repository Pattern · Dependency Injection

---

## Papéis de usuário (RBAC)

| Papel | Descrição |
|-------|-----------|
| `CUSTOMER` | Cria pedidos e acompanha o rastreamento dos próprios pedidos |
| `DRIVER` | Recebe pedidos para entrega e envia pings de GPS |
| `ADMIN` | Gerencia todos os recursos do sistema |

---

## Rodando o projeto

**Pré-requisito:** Docker e Docker Compose instalados.

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Projeto-Rastreamento.git
cd Projeto-Rastreamento

# Crie o arquivo de variáveis de ambiente
cp .env.example .env
# edite o .env com suas credenciais

# Suba os containers
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.  
Documentação interativa: `http://localhost:8000/docs`

---

## Rotas disponíveis

### Auth
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| POST | `/api/v1/auth/login` | Público | Login e geração de token |
| POST | `/api/v1/auth/refresh-token` | Autenticado | Renovar token de acesso |
| GET | `/api/v1/auth/me` | Autenticado | Dados do usuário autenticado |

### Users
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| POST | `/api/v1/users/` | Público | Cadastro de novo usuário |
| GET | `/api/v1/users/` | Admin | Listar todos os usuários (paginado) |
| GET | `/api/v1/users/{user_id}` | Admin | Buscar usuário por ID |
| GET | `/api/v1/users/get-by-email/{email}` | Admin | Buscar usuário por email |
| PUT | `/api/v1/users/{user_id}` | Próprio usuário / Admin | Atualizar usuário |
| DELETE | `/api/v1/users/{user_id}` | Próprio usuário / Admin | Deletar usuário |

### Addresses
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| GET | `/api/v1/addresses/` | Admin | Listar todos os endereços (paginado) |
| GET | `/api/v1/addresses/{address_id}` | Admin | Buscar endereço por ID |
| GET | `/api/v1/addresses/get-by-cep/{cep}` | Admin / Driver | Buscar endereços por CEP (paginado) |
| PUT | `/api/v1/addresses/{address_id}` | Proprietário / Admin | Atualizar endereço |

### Orders
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| GET | `/api/v1/orders/` | Admin / Driver | Listar todos os pedidos (paginado) |
| GET | `/api/v1/orders/{order_id}` | Admin / Driver | Buscar pedido por ID |
| GET | `/api/v1/orders/get-by-status/{status}` | Todos | Pedidos por status — Customer vê apenas os próprios |
| GET | `/api/v1/orders/get-by-user/{user_id}` | Próprio usuário / Admin | Pedidos de um usuário (paginado) |
| POST | `/api/v1/orders/` | Customer / Admin | Criar pedido |
| PUT | `/api/v1/orders/{order_id}` | Admin / Driver | Atualizar pedido |
| DELETE | `/api/v1/orders/{order_id}` | Admin | Deletar pedido |

### Tracking
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| GET | `/api/v1/tracking/` | Admin | Listar todos os registros (paginado) |
| GET | `/api/v1/tracking/{tracking_id}` | Admin / Driver | Buscar registro por ID |
| GET | `/api/v1/tracking/get-by-order/{order_id}` | Todos | Histórico de pings de um pedido (paginado) |
| GET | `/api/v1/tracking/get-latest-by-order/{order_id}` | Todos | Última localização de um pedido |
| POST | `/api/v1/tracking/` | Admin / Driver | Registrar ping de GPS |

**Status de pedido disponíveis:** `Pending` · `Shipped` · `Delivered` · `Cancelled`

---

## Modelos de dados

```
User ────────── Address       (1:1, FK no User)
User ────────── DriverProfile (1:1, FK no DriverProfile)
User ────────── Orders        (1:N)
Order ───────── Tracking      (1:N, pings de GPS)
Address ─────── Orders        (1:N, endereço de entrega)
```

---

## Status do projeto

### Concluído
- [x] Modelos base (User, Address, Order, Tracking)
- [x] Autenticação JWT com refresh token
- [x] RBAC com papéis (Customer, Driver, Admin)
- [x] Paginação em todas as rotas de listagem
- [x] Rate limiting no cadastro e login
- [x] Hash de senha com Argon2
- [x] CORS configurado
- [x] Docker + Docker Compose com healthcheck
- [x] Exceções customizadas com handler global
- [x] Model DriverProfile

### Em desenvolvimento
- [ ] Schema, repository, service e router do DriverProfile
- [ ] Order enriquecido (description, weight, tracking_code, endereço de origem/destino, driver, datas)
- [ ] Tracking enriquecido (event_type, description, location_name)
- [ ] OrderStatusHistory — log de mudanças de status
- [ ] Validação de transição de status (máquina de estados)
- [ ] Rota pública `GET /track/{tracking_code}` (sem autenticação)

### Planejado
- [ ] Filtros avançados nas listagens (data, cidade, status, driver)
- [ ] Dashboard de estatísticas para admin
- [ ] Testes de integração
- [ ] Notificações por email
- [ ] WebSocket para tracking em tempo real
- [ ] Redis para cache
- [ ] Kafka para mensageria de eventos

---

## Segurança implementada

- Autenticação via Bearer Token (JWT)
- Senhas hasheadas com Argon2 via pwdlib
- Rate limiting: 5 req/min no login, 3 req/min no cadastro
- Verificação de propriedade de recursos (usuário só acessa o próprio)
- Separação de papéis com 403 Forbidden para acesso não autorizado
- Rotas administrativas protegidas por papel ADMIN
