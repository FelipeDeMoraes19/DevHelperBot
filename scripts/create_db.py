import asyncio
import asyncpg
from app.config.database import Base, engine
from app.models import conversation, feedback, user

DB_USER = "devhelper"
DB_PASSWORD = "secretpassword"
DB_HOST = "postgres"
DB_PORT = "5432"
DB_NAME = "devhelper_test"

ROOT_DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

async def ensure_db_exists():
    """
    Conecta ao database 'postgres' e cria o database devhelper_test se ainda não existir.
    """
    conn = await asyncpg.connect(ROOT_DSN)
    exists = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname = $1",
        DB_NAME
    )
    if not exists:
        print(f"Database '{DB_NAME}' não existe. Criando agora...")
        await conn.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"Database '{DB_NAME}' criado com sucesso!")
    else:
        print(f"Database '{DB_NAME}' já existe.")
    await conn.close()

async def init_db():
    await ensure_db_exists()

    async with engine.begin() as conn:
        print("Criando tabelas em devhelper_test...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tabelas criadas com sucesso!")
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
