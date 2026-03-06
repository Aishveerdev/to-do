from fastapi import FastAPI, Depends
from crud import crud
from services.database import get_db, engine, Base
from schemas.task_schema import taskUpdate , taskResponse , taskCreate
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from models.user_model import User
from utils.jwt_management import get_current_user
from routers import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield

app = FastAPI(lifespan=lifespan)


@app.get("/") # Home page
async def read_root():
    return {"message": "Welcome to the To-Do API!"}

@app.post("/tasks", response_model=taskResponse) # Create TASK
async def create_task(task:taskCreate ,db: AsyncSession = Depends(get_db) , current_user: User = Depends(get_current_user)):
    return await crud.create_task(db, task ,current_user)

@app.get("/tasks", response_model=list[taskResponse]) # Get all tasks
async def get_tasks(db: AsyncSession = Depends(get_db) , current_user: User = Depends(get_current_user)):
    return await crud.get_tasks(db, current_user)

@app.get("/tasks/{task_id}", response_model=taskResponse) # Get single task
async def get_task(task_id: int , db: AsyncSession = Depends(get_db) , current_user: User = Depends(get_current_user)):
    return await crud.get_task(db, task_id , current_user) 
 #here we called the " get_current_user" fucntion and injected it in "User" , now the user is passed to crud function.


@app.put("/tasks/{task_id}", response_model=taskResponse) # Update single task
async def update_task(task_id: int, task_update: taskUpdate, db: AsyncSession = Depends(get_db) , current_user: User = Depends(get_current_user)):
    return await crud.update_task(db, task_id, current_user , task_update)

@app.delete("/tasks/{task_id}" ) # Delete single task
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db) , current_user: User = Depends(get_current_user)):

    return await crud.delete_task(db, task_id)


app.include_router(auth_router.router,prefix="/auth" , tags=["Authentication"]) # here we included the auth router in our main app.




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)