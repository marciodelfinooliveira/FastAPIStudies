### Estrutura do Projeto
.
├── app/
│   ├── api/
│   │   ├── deps.py             # Injeção de dependências
│   │   └── v1/
│   │       ├── api.py          # Agregador de todas as rotas da v1
│   │       └── endpoints/
│   │           └── users.py    # Rotas relacionadas a usuários (/users, /users/{id})
│   ├── core/
│   │   ├── config.py           # Configurações centralizadas (usando Pydantic Settings)
│   │   └── security.py         # Funções de hash de senha e criação/validação de JWT
│   ├── db/
│   │   ├── base.py             # Base declarativa do SQLAlchemy para os modelos
│   │   ├── models/
│   │   │   └── user.py         # Modelo ORM do SQLAlchemy para a tabela de usuários
│   │   └── session.py          # Engine e gerenciamento de sessão assíncrona do DB
│   ├── schemas/
│   │   ├── token.py            # Esquemas Pydantic para o token JWT
│   │   └── user.py             # Esquemas Pydantic (validação) para usuários
│   ├── services/
│   │   └── user_service.py     # Lógica de negócio (CRUD e outras operações)
│   └── main.py                 # Ponto de entrada da aplicação FastAPI
│
├── alembic/                    # Diretório de migrações do Alembic
│
├── alembic.ini                 # Arquivo de configuração do Alembic
├── docker-compose.yaml
├── Dockerfile
├── entrypoint.sh
├── .env
└── .gitignore