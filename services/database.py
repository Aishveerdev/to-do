from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker , declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./to_do.db"

# Creates a connecion to dtatase
engine = create_async_engine(DATABASE_URL, echo=True)
# Like a phone call to database , we can use this session to interact with database
AsyncSessionLocal = sessionmaker(bind=engine , class_=AsyncSession, expire_on_commit=False)
#this base contian sall the database related setup and will create an object that we can use to create our database models
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Create the database tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)