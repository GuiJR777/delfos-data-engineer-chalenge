Esse repositorio tem por objetivo entregar o desafio de Data Engineer da
Delfos, com API FastAPI, ETL diário e orquestração via Dagster.
Enunciado do desafio: [challenge/README.md](challenge/README.md)

**Quick Start**
1. `make up`
2. `make seed SEED_ARGS="--truncate"`
3. `make etl DATE=YYYY-MM-DD`

**Arquitetura**
![Arquitetura](dev\image.png)

**Detalhes**

**Pre-requisitos**
- Docker Desktop (Docker Compose)
- Python 3.11+
- Make (GNU Make)

**Seed do banco fonte**
- `make seed`
- `make seed SEED_ARGS="--start-date YYYY-MM-DD --days 10 --truncate"`
- O intervalo gerado fica em `seed_info.json` com `start_ts` e `end_ts`

**API**
- Health: `GET /health`
- Data: `GET /data` com `start`, `end`, `signals`, `limit`, `offset`
- Sinais permitidos: `wind_speed`, `power`, `ambient_temperature`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**ETL**
- Rodar por data: `make etl DATE=YYYY-MM-DD`
- Usa `API_BASE_URL` e `TARGET_DATABASE_URL` do `.env`
- Agrega em 10 min (mean, min, max, std) e grava no alvo

**Dagster**
- Subir local: `make dagster`
- Subir via Docker: `make up`
- UI: `http://localhost:3000`
- Asset diario: `daily_etl` com particoes diarias
- Schedule: `0 1 * * *`

**Makefile**
- `make setup`
- `make up`
- `make down`
- `make reset`
- `make logs`
- `make ps`
- `make health`
- `make seed`
- `make api`
- `make etl DATE=YYYY-MM-DD`
- `make dagster`
- `make test`

**Checagens finais**
1. `make reset`
2. `make up`
3. `make seed SEED_ARGS="--truncate"`
4. `make etl DATE=YYYY-MM-DD`
5. `make health`
